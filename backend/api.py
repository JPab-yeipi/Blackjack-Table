from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from deck import Deck, Card
from players import Player

app = FastAPI()

# Allow CORS (for frontend dev/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INITIAL_PLAYER_BALANCE = 500.0
MIN_BET = 100.0

# -------- State --------
game_sessions: Dict[str, Dict] = {}

# -------- Schemas --------
class StartRequest(BaseModel):
    name: str

class BetRequest(BaseModel):
    session_id: str
    bet: float

class ActionRequest(BaseModel):
    session_id: str
    action: str  # "hit" or "stand"

class StateResponse(BaseModel):
    session_id: str
    player_balance: float
    player_hand: List[str]
    player_hand_value: int
    croupier_hand: List[str]
    croupier_visible_hand: List[str]
    croupier_hand_value: Optional[int]
    current_bet: float
    status: str
    msg: Optional[str] = None
    finished: bool

# -------- Helper Functions --------
def hand_to_str(hand):
    return [str(c) for c in hand]

def get_session(session_id: str):
    session = game_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid session_id")
    return session

def new_session(name: str) -> str:
    import uuid
    session_id = str(uuid.uuid4())
    player = Player(name, money=INITIAL_PLAYER_BALANCE)
    croupier = Player("Croupier")
    deck = Deck()
    deck.shuffle()
    session = {
        "player": player,
        "croupier": croupier,
        "deck": deck,
        "status": "betting",  # or 'playing', 'round_over', 'finished'
        "msg": None,
        "current_bet": 0.0,
        "finished": False
    }
    game_sessions[session_id] = session
    return session_id

def session_state(session_id: str, reveal_all=False, msg=None) -> StateResponse:
    session = get_session(session_id)
    player = session["player"]
    croupier = session["croupier"]
    status = session["status"]
    finished = session.get("finished", False)
    current_bet = player.current_bet

    croupier_all = hand_to_str(croupier.hand)
    if reveal_all or status == 'round_over' or finished:
        croupier_visible = hand_to_str(croupier.hand)
        croupier_hand_value = croupier.hand_value
    else:
        croupier_visible = [str(croupier.hand[0])] + ['Hidden'] * (len(croupier.hand)-1) if len(croupier.hand) > 0 else []
        croupier_hand_value = None

    return StateResponse(
        session_id=session_id,
        player_balance=player.balance,
        player_hand=hand_to_str(player.hand),
        player_hand_value=player.hand_value,
        croupier_hand=croupier_all,
        croupier_visible_hand=croupier_visible,
        croupier_hand_value=croupier_hand_value,
        current_bet=current_bet,
        status=status,
        msg=msg if msg else session.get("msg"),
        finished=finished
    )

def restart_round(session):
    player = session["player"]
    croupier = session["croupier"]
    deck = session["deck"]
    player.restart_hand()
    croupier.restart_hand()
    if deck.num_cards < 5:
        deck()
        deck.shuffle()
    session["status"] = "betting"
    session["finished"] = False
    session["msg"] = ""
    player._current_bet = 0.0

# -------- API Endpoints --------
@app.post("/start", response_model=StateResponse)
def start_game(req: StartRequest):
    session_id = new_session(req.name)
    return session_state(session_id, msg=f"Welcome {req.name}! Place your bet.")

@app.post("/bet", response_model=StateResponse)
def place_bet(req: BetRequest):
    session = get_session(req.session_id)
    player = session["player"]
    croupier = session["croupier"]
    deck = session["deck"]

    if session["status"] != "betting":
        raise HTTPException(status_code=400, detail="Not accepting bets right now.")

    if player.balance < MIN_BET:
        session["status"] = "finished"
        session["finished"] = True
        return session_state(req.session_id, msg="You don't have enough funds to continue playing. Game over.")

    if req.bet < MIN_BET:
        raise HTTPException(status_code=400, detail=f"Minimum bet is {MIN_BET}.")

    try:
        player.place_bet(req.bet)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    player.hit(deck)
    croupier.hit(deck)

    # Blackjack on initial deal
    if player.hand_value == 21:
        player.award_winnings(2.5)
        session["status"] = "round_over"
        session["finished"] = False
        session["msg"] = f"Blackjack! {player.name} wins!"
        return session_state(req.session_id, reveal_all=True)
    else:
        session["status"] = "playing"
        return session_state(req.session_id, msg="Choose action: hit or stand.")

@app.post("/action", response_model=StateResponse)
def player_action(req: ActionRequest):
    session = get_session(req.session_id)
    player = session["player"]
    croupier = session["croupier"]
    deck = session["deck"]

    if session["status"] not in ["playing"]:
        raise HTTPException(status_code=400, detail="Not ready for action now.")

    if req.action == "hit":
        player.hit(deck)
        if player.hand_value > 21:
            player.award_winnings(0)
            session["status"] = "round_over"
            session["msg"] = "Bust! Croupier wins!"
            return session_state(req.session_id, reveal_all=True)
        elif player.hand_value == 21:
            # Player stands automatically with 21
            session["status"] = "croupier"
        else:
            return session_state(req.session_id, msg="You chose hit.")
    
    if req.action == "stand" or (req.action == "hit" and player.hand_value == 21):
        # Croupier's turn
        session["status"] = "croupier"
        croupier.play(deck)
        player_total = player.hand_value
        dealer_total = croupier.hand_value

        msg = ""
        if dealer_total > 21:
            player.award_winnings(2)
            msg = f"{croupier.name} busts! {player.name} wins!"
        elif player_total > dealer_total:
            player.award_winnings(2)
            msg = f"{player.name} wins!"
        elif player_total < dealer_total:
            player.award_winnings(0)
            msg = f"{croupier.name} wins!"
        else:
            player.award_winnings(1)
            msg = "It's a push (tie)!"
        session["status"] = "round_over"
        session["msg"] = msg
        return session_state(req.session_id, reveal_all=True)
    
    return session_state(req.session_id)

@app.post("/restart", response_model=StateResponse)
def restart(req: ActionRequest):
    session = get_session(req.session_id)
    if session["player"].balance < MIN_BET:
        session["status"] = "finished"
        session["finished"] = True
        return session_state(req.session_id, msg="Not enough funds to continue. Game over.")
    restart_round(session)
    return session_state(req.session_id, msg="Round restarted. Place your bet.")

@app.get("/state/{session_id}", response_model=StateResponse)
def get_state(session_id: str):
    return session_state(session_id)