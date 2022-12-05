# check if user type appropriate value for amount of pages
def check_input():
    while True:
        user_input = input("How many pages do you want to scrape: ")
        try:
            page_val = abs(int(user_input))
            if 0 < page_val < 15:
                return page_val
            elif page_val == 0:
                print("You've just typed zero . Plz try some higher value ")
                continue
            else:
                print("Hold down your value is too high , do not overload servers )  . Plz try some lower  value ")
        except ValueError:
            try:
                val = float(user_input)
                print(f"'{val}' is a float  number. Plz try again")
            except ValueError:
                print(f"No '{user_input}' input is not a number. It's a string. Plz try again")
