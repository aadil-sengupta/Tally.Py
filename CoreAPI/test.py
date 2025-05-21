from xmlFunctions import TallyClient

tally = TallyClient()

print(tally.test_connection())

print(tally.get_current_company())
