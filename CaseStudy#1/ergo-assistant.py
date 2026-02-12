"""
Ergonomic Configuration Assistant Prototyp
"""
from dataclasses import dataclass, field
import profile

@dataclass
class UserProfile:
    hand_size: str
    grip_style: str
    session_duration: int
    discomfort_level: str
    keyboard_layout: str
    mouse_weight: int | None
    space_issue: str
    game_type: str

    #Derived attributes
    risk_points: int=0
    risk_level: str="none"
    recommendations: list[str]=field(default_factory=list)
    
    #Convenience attributes for risk assessment
    has_wrist_pain: bool = False
    has_finger_pain: bool = False
    has_forearm_pain: bool = False
    
# Input helper functions    
def ask_choise(prompt: str, choices: list[str]) -> str:
    """Prompt user until they enter a valid choice."""
    allowed = {c.lower(): c for c in choices}
    while True:
        ans = input(f"{prompt} ({'/'.join(choices)}): ").strip().lower()
        if ans in allowed:
            return ans
        print(f"Invalid choice. Please choose from: {', '.join(choices)}.")
        
        
def ask_int(prompt: str, min_val: int = None, max_val: int = 10**9) -> int:
    """Promput user until they enter a valid integer within the specified range."""
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
def ask_mouse_weight() -> int | None:
    """Ask user for mouse weight, allowing for 'don't know'."""
    while True:
        raw = input("What is the weight of your mouse in grams? (or type 'don't know'): ").strip().lower()
        if raw == "don't know":
            return None
        try:
            weight = int(raw)
            if 200 >= weight >= 20:
                return weight
            print("Weight must be a realistic value (20-200g) or 'don't know'.")
        except ValueError:
            print("Invalid input. Please enter a valid integer or 'don't know'.")
            
# Analysis & rules
def parse_discomfort(profile: UserProfile) -> None:
    """Keyword parsing for discomfort level to set pain flags."""
    text = profile.discomfort_level.lower()
    profile.has_wrist_pain = "wrist" in text
    profile.has_finger_pain = "finger" in text or "fingers" in text
    profile.has_forearm_pain = "forearm" in text
    if "none" in text:
        profile.has_wrist_pain = False
        profile.has_finger_pain = False
        profile.has_forearm_pain = False
        
def add_recommendation(profile: UserProfile, msg: str) -> None:
    """Add a recommendation to the profile if it's not already present."""
    if msg not in profile.recommendations:
        profile.recommendations.append(msg)
        
def evaluate(profile: UserProfile) -> None:
    """Rule based evaluation of the user profile to determine risk points, level, and recommendations."""
    parse_discomfort(profile)
    
    # Session length contributes to risk
    if profile.session_duration >= 180:
        profile.risk_points += 2
        add_recommendation(profile, "Long sessions detected: add structured 5-10 minute breaks every 45-60 minutes.")
    elif profile.session_duration >= 90:
        profile.risk_points += 1
        add_recommendation(profile, "Consider adding regular breaks to your gaming sessions.")
        
    # Discomfort contributes to risk
    if profile.has_wrist_pain:
        profile.risk_points += 2
        add_recommendation(profile, "Wrist discomfort: consider a lighter mouse, neutral wrist position (avoid excessive extension), and wrist support. ")
        add_recommendation(profile, "Try slight keyboard angle adjustment to keep wrists straight.")
    if profile.has_finger_pain:
        profile.risk_points += 1
        add_recommendation(profile, "Finger discomfort: consider a mouse with a more ergonomic shape that supports your hand size better.")
        add_recommendation(profile, "Finger discomfort: consider lighter actuation force for keys and mouse buttons.")
    if profile.has_forearm_pain:
        profile.risk_points += 1
        add_recommendation(profile, "Forearm discomfort: ensure your chair and desk height allow for a 90-degree angle at the elbow.")
        
    # Hand size and grip style contributes to mouse shape/size recommendations
    if profile.hand_size == "small" and profile.grip_style == "fingertip":
        add_recommendation(profile, "Small hand + fingertip grip: consider a smaller, lighter mouse (40-70g) with a shape that allows for easy fingertip control.")
    elif profile.hand_size == "medium" and profile.grip_style == "fingertip":
        add_recommendation(profile, "Medium hand + fingertip grip: consider a lighter medium-sized mouse (50-80g) with a shape that allows for easy fingertip control.")
    elif profile.hand_size == "large" and profile.grip_style == "fingertip":
        add_recommendation(profile, "Large hand + fingertip grip: consider a medium-sized mouse (60-90g) with a shape that allows for easy fingertip control.")
    elif profile.hand_size == "small" and profile.grip_style == "claw":
        add_recommendation(profile, "Small hand + claw grip: consider a smaller mouse (40-70g) with a shape that supports the arch of your hand and allows for easy claw grip.")
    elif profile.hand_size == "medium" and profile.grip_style == "claw":
        add_recommendation(profile, "Medium hand + claw grip: consider a medium-sized mouse (50-80g) with a shape that supports the arch of your hand and allows for easy claw grip.")
    elif profile.hand_size == "large" and profile.grip_style == "claw":
        add_recommendation(profile, "Large hand + claw grip: consider a medium to larger mouse (60-100g) with a shape that supports the arch of your hand and allows for easy claw grip.")
    elif profile.hand_size == "small" and profile.grip_style == "palm":
        add_recommendation(profile, "Small hand + palm grip: consider a smaller mouse (40-70g) with a shape that allows your palm to rest comfortably on the rear of the mouse.")
    elif profile.hand_size == "medium" and profile.grip_style == "palm":
        add_recommendation(profile, "Medium hand + palm grip: consider a medium-sized mouse (50-80g) with a shape that allows your palm to rest comfortably on the rear of the mouse.")
    elif profile.hand_size == "large" and profile.grip_style == "palm":
        add_recommendation(profile, "Large hand + palm grip: consider a medium to larger mouse (60-100g) with a shape that allows your palm to rest comfortably on the rear of the mouse.")
        
    # Mouse weight contributes to risk
    if profile.mouse_weight is not None:
        if profile.mouse_weight > 95:
            profile.risk_points += 1
            add_recommendation(profile, "Heavy mouse detected: consider switching to a lighter mouse (50-80g) to reduce strain.")
        elif profile.mouse_weight > 70:
            profile.risk_points += 1
            add_recommendation(profile, "Consider switching to a lighter mouse (50-70g) to reduce strain.")
        elif profile.mouse_weight <= 60:
            add_recommendation(profile, "Your mouse weight is within a good range for ergonomic gaming.")
    else:
        add_recommendation(profile, "Mouse weight unknown: if you experience discomfort, consider checking your mouse weight.")
        
    #keyboard layout contributes to wrist position recommendations
    if profile.keyboard_layout == "wasd" and profile.hand_size == "large":
        add_recommendation(profile, "Large hands: consider trying ESDf for more key reach and centralized hand position.")
    elif profile.keyboard_layout == "esdf" and profile.hand_size == "small":
        add_recommendation(profile, "Small hands: consider trying WASD for more compact key reach and centralized hand position.")
    if profile.space_issue == "yes":
        add_recommendation(profile, "Space constraints: consider a compact keyboard layout (e.g. 60% or 65%) and a larger mousepad to allow for better mouse positioning and reduce shoulder strain.")
        
    # Game type contributes to break and posture recommendations
    if profile.game_type == "fps":
        add_recommendation(profile, "FPS focus: prioritize consistent sensitivity and a comfortable mouse grip to reduce micro-adjustment strain.")
    elif profile.game_type == "moba":
        add_recommendation(profile, "MOBA focus: consider a mouse with good button placement for quick access to abilities and macros.")
    elif profile.game_type == "rpg":
        add_recommendation(profile, "RPG focus: consider a mouse with good comfort for longer sessions and customizable buttons for inventory management.")
    elif profile.game_type == "mmorpg":
        add_recommendation(profile, "MMORPG focus: consider a mouse with good comfort for longer sessions and customizable buttons for inventory management and macros.")
    elif profile.game_type == "other":
        add_recommendation(profile, "General gaming: focus on overall comfort, proper breaks, and ergonomic posture to reduce strain across various game types.")
        
    # Final risk level assessment
    if profile.risk_points >= 5:
        profile.risk_level = "high"
    elif profile.risk_points >= 3:
        profile.risk_level = "moderate"
    elif profile.risk_points >= 1:
        profile.risk_level = "mild"
    else:
        profile.risk_level = "none"
        
# UI program flow
def print_results(profile: UserProfile) -> None:
    print("\n" + "=" * 50)
    print("Ergonomic Configuration Summary")
    print("=" * 50)
    print(f"Hand size: {profile.hand_size}")
    print(f"Grip style: {profile.grip_style}")
    print(f"Session duration: {profile.session_duration} minutes")
    print(f"Discomfort notes: {profile.discomfort_level.strip() or '(none given)'}")
    print(f"Keyboard layout: {profile.keyboard_layout}")
    print(f"Mouse weight: {profile.mouse_weight if profile.mouse_weight is not None else '(unknown)'} grams")
    print(f"Space constraints: {profile.space_issue}")
    print(f"Game type: {profile.game_type}")
    print(f"\nRisk level: {profile.risk_level.upper()} (Points: {profile.risk_points})")
    print("\nRecommendations:")
    if not profile.recommendations:
        print("- No specific recommendations. Your current setup appears to be low risk.")
    else:
        for rec in profile.recommendations:
            print(f"- {rec}")
    print("=" * 50 + "\n")
    
def main():
    print("Welcome to the Ergonomic Configuration Assistant Prototype!")
    print("Answer a few questions about your gaming setup and habits to receive personalized ergonomic recommendations.\n")
    
    hand_size = ask_choise("What is your hand size?", ["small", "medium", "large"])
    grip_style = ask_choise("What is your primary mouse grip style?", ["fingertip", "claw", "palm"])
    session_duration = ask_int("On average, how long are your gaming sessions in minutes?", min_val=1)
    discomfort_level = input("Do you experience any discomfort while gaming? If so, please describe (e.g. 'wrist pain', 'finger discomfort', 'forearm ache', or 'none'): ").strip()
    keyboard_layout = ask_choise("What keyboard layout do you use for gaming?", ["wasd", "esdf", "other"]).lower()
    mouse_weight = ask_mouse_weight()
    space_issue = ask_choise("Do you have space constraints at your gaming setup?", ["yes", "no"])
    game_type = ask_choise("What type of games do you primarily play?", ["fps", "moba", "rpg", "mmorpg", "other"])
    
    profile = UserProfile(
        hand_size=hand_size,
        grip_style=grip_style,
        session_duration=session_duration,
        discomfort_level=discomfort_level,
        keyboard_layout=keyboard_layout,
        mouse_weight=mouse_weight,
        space_issue=space_issue,
        game_type=game_type
    )
    
    evaluate(profile)
    print_results(profile)
    
if __name__ == "__main__":
    main()