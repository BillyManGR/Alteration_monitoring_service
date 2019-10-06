def try_and_fix(raw):
    hands_on = hands_off = cook_time = portions = difficulty = ""
    print(raw)
    for i in range(1, len(raw), 2):
        print(i)
        if raw[i] == "Ηands on" or raw[i] == "Χρόνος Εκτέλεσης":
            hands_on = raw[i-1]
        elif raw[i] == "Hands off" or raw[i] == "Χρόνος Αναμονής":
            hands_off = raw[i-1]
        elif raw[i] == "Cook Time" or raw[i] == "Χρόνος Ψησίματος":
            cook_time = raw[i-1]
        elif raw[i] == "Portion(s)" or raw[i] == "Μερίδες":
            portions = raw[i-1]
        elif raw[i] == "Difficulty" or raw[i] == "Βαθμός Δυσκολίας":
            difficulty = raw[i-1]
        else:
            print("Shitty HTML")
            del raw[i-1]
            hands_on, hands_off, cook_time, portions, difficulty = try_and_fix(raw)
    return hands_on, hands_off, cook_time, portions, difficulty


raw = ['30 λεπτά', 'Χρόνος Εκτέλεσης', '30 λεπτά', 'Χρόνος Αναμονής', '10-12', 'Μερίδες', '1', 'Βαθμός Δυσκολίας']

print(try_and_fix(raw))
