from botNotification import send_message

# https://marketplace.axieinfinity.com/axie?class=Reptile&stage=4&pureness=5&breedCount=0&breedCount=1
payload = {"operationName":"GetAxieBriefList","variables":{"from":0,"size":24,"sort":"PriceAsc","auctionType":"Sale","owner":None,"criteria":{"region":None,"parts":None,"bodyShapes":None,"classes":["Reptile"],"stages":[4],"numMystic":None,"pureness":[5],"title":None,"breedable":None,"breedCount":[0,1],"hp":[],"skill":[],"speed":[],"morale":[]}},"query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"}
filter = "[Reptil 🦎 - Pureza 5 - Breed count 0 a 1](https://marketplace.axieinfinity.com/axie?class=Reptile&stage=4&pureness=5&breedCount=0&breedCount=1)"

send_message(payload, filter, True)