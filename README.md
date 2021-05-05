# discordbot
This is a Discord bot I wrote for fun for a personal groupchat. It has a couple games to play and a DiscordDollar system implemented with a SQLite database, in which users gain DiscordDollars for participation in the chat and for winning games. DiscordDollars can be traded for (imaginary) Bitcoin based on the (real) price thereof. The bot also employs web scraping for word lookup, translation, and comic fetching (which also costs DiscordDollars).  

## Commands:  
`MINESWEEPER`: generate Minesweeper board  
`CONNECT FOUR`: play Connect 4  
`GARFIELD PLEASE`: random Garfield strip  
`DILBERT PLEASE`: random Dilbert strip  
`CALVIN AND HOBBES PLEASE`: random C&H  
`$comic [comic]`: random comic from GoComics  
`$ety [word]`: etymology lookup  
`$def [word]`: dictionary lookup  
`$udef [word]`: Urban Dictionary lookup  
`$bitcoin`: get current btc price  
`$bitcoinx [xxx]`: get btc price in foreign currency  
`$buybitcoin [amount]`: buy Bitcoin with DiscordDollars  
`$sellbitcoin [amount]`: sell Bitcoin for DiscordDollars  
`$send [@user] [amount] [dd, btc]`: send BTC or DD to another user  
`$trans "your message here" [language]`: translate message  
`$dd`: check your DiscordDollars balance  
`$chromecode`: get a code to link the Chrome extension to Discord  
`$help`: show commands  
