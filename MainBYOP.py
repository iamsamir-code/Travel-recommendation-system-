# AI-Based Travel Recommendation System (CLI)
places = [
    {"name": "Goa", "type": "beach", "budget": "medium", "season": "winter", "group": ["friends","solo"], "faith": "none"},
    {"name": "Manali", "type": "mountains", "budget": "low", "season": "summer", "group": ["friends","family"], "faith": "none"},
    {"name": "Rishikesh", "type": "spiritual", "budget": "low", "season": "all", "group": ["solo","friends"], "faith": "hindu"},
    {"name": "Ajmer", "type": "spiritual", "budget": "low", "season": "winter", "group": ["family"], "faith": "muslim"},
    {"name": "Amritsar", "type": "spiritual", "budget": "low", "season": "winter", "group": ["family"], "faith": "sikh"},
    {"name": "Bodh Gaya", "type": "spiritual", "budget": "low", "season": "winter", "group": ["solo"], "faith": "buddhist"},
    {"name": "Velankanni", "type": "spiritual", "budget": "low", "season": "winter", "group": ["family"], "faith": "christian"},
    {"name": "Kerala", "type": "nature", "budget": "medium", "season": "winter", "group": ["family","couple"], "faith": "none"},
    {"name": "Jaipur", "type": "heritage", "budget": "medium", "season": "winter", "group": ["family"], "faith": "none"},
    {"name": "Ahemdabad", "type": "heritage", "budget": "medium", "season": "winter", "group": ["family"], "faith": "none"},
    {"name": "kutch", "type": "heritage", "budget": "medium", "season": "winter", "group": ["family"], "faith": "none"},
    {"name": "agra & fatehpur sikri", "type": "heritage", "budget": "medium", "season": "winter", "group": ["family", "couple"], "faith": "muslim"},
    {"name": "srinagar", "type": "nature", "budget": "high", "season": "monsoon", "group": ["couple","family"], "faith": "none"}
]
history = []

# INPUT 
def getin(prompt, options):
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return value
        print("Invalid input")

# SIMPLE LEARNING 
def preference():
    if not history:
        return None

    count = {}
    for h in history:
        t = h["type"]
        if t not in count:
            count[t] = 1
        else:
            count[t] += 1

    # find max manually (no Counter, no shortcuts)
    max_typ = None
    max_val = 0

    for key in count:
        if count[key] > max_val:
            max_val = count[key]
            max_typ = key

    return max_typ

# SCORING 
def calculatescore(place, user, learned_type):
    score = 0
    reason = []

    if place["budget"] == user["budget"]:
        score += 20
        reason.append("budget")
    if place["type"] == user["type"]:
        score += 25
        reason.append("type")
    if place["season"] == user["season"] or place["season"] == "all":
        score += 20
        reason.append("season")
    if user["group"] in place["group"]:
        score += 15
        reason.append("group")
    # learning effect
    if learned_type and place["type"] == learned_type:
        score += 10
        reason.append("learned")

    return score, reason

# RECOMMEND
def recommend():
    print("\nEnter preferences:")

    user = {
    "budget": getin("Budget (low/medium/high): ", ["low","medium","high"]),
    "type": getin("Type (beach/mountains/spiritual/nature/heritage): ", ["beach","mountains","spiritual","nature","heritage"]),
    "season": getin("Season (summer/winter/monsoon/all): ", ["summer","winter","monsoon","all"]),
    "group": getin("Group (solo/friends/family): ", ["solo","friends","family"])
     }
    religious = getin("Religious? (yes/no): ", ["yes","no"])
    faith = None

    if religious == "yes":
        faith = getin("Faith: ", ["hindu","muslim","sikh","buddhist","christian"])

    # filtering
    filtered = []
    for p in places:
        if religious == "yes":
            if p["type"] == "spiritual" and p["faith"] == faith:
                filtered.append(p)
        else:
            filtered.append(p)

    if religious == "yes" and not filtered:
        print("No places found")
        return

    learned = preference()

    results = []

    for p in filtered:
        score, reason = calculatescore(p, user, learned)
        results.append({"place": p, "score": score, "reason": reason})
    # sorting (simple)
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            if results[j]["score"] > results[i]["score"]:
                results[i], results[j] = results[j], results[i]
    print("\nTop Recommendations:")
    for r in results[:3]:
        print(r["place"]["name"], "- Score:", r["score"])
        print("Reason:", ", ".join(r["reason"]))
        print()
    # store history
    if results:
        top = results[0]["place"]
        history.append({
            "type": top["type"],
            "budget": top["budget"],
            "season": top["season"]
        })

# MENU
def main():
    while True:
        print("\n1. Recommend\n2. Places\n3. History\n4. Exit")
        ch = input("Choice: ")

        if ch == "1":
            recommend()
        elif ch == "2":
            for p in places:
                print(p["name"])
        elif ch == "3":
            if not history:
                print("No history")
            else:
                print("\nHistory:")
                for i, h in enumerate(history, 1):
                    print(i, "->", h)
        elif ch == "4":
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()