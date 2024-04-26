conv = [
    "<Opponent>If you are not advising your companies to get the cash out, then you are not doing your job as a Board Member or as a Shareholder.  Daily life in startups is risky enough, don’t play with your lifeline… </Opponent>",
    "<Opponent>Easy to say when it is not your company money dude</Opponent>",
]

output = ""
for i, c in enumerate(conv):
    if i % 2 == 1:
        c = "<You>" + c + "</You>"
    output += c

print(output)
