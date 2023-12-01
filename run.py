from booking.booking import Booking

# inst=Booking()            #for testing
# inst.land_first_page()    #for testing
# using Booking(use_cache=True) in line 7, will open the browser in debug mode and connect to it, this may cause unwanted behaviour as logic to handle cached information is not written.
# Booking(teardown=True) will automatically close the browser

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='GBP')
        bot.select_place_to_go(input("Where do you want to go?"))
        bot.select_dates(check_in_date=input("What's the check in date(yyyy-mm-dd)?"), check_out_date=input("What's the check in date(yyyy-mm-dd)?"))
        bot.select_count(adult=4, rooms=2)
        bot.click_search()
        bot.apply_filtration()  # Needs work to work properly while using cache and cookies
        bot.refresh()           # There is a better workaround using ExpectedConditions...
        bot.report_results()
except Exception as e:
    print("\n\nSomething went wrong... :/\n\n")
    if 'in PATH' in str(e):
        print("An old selenium error...")
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '   set PATH=%PATH%;C:path-to-your-foler \n \n'
            'Linux: \n'
            '   PATH=$PATH:/path/toyour/folder/ \n'
        )
    else: 
        raise
    