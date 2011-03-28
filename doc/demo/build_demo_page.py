from dialogs.parsing.parser import Parser

parser = Parser()

print """
<html>
    <head>
      <meta charset="UTF-8">
      <title> DIALOGS parser demo</title>
      <link rel ="stylesheet" type="text/css" href="styles.css" title="Style"></link>
      <link rel="stylesheet" href="javascript/jquery.tooltip.css" />

      <script src="javascript/lib/jquery.js" type="text/javascript"></script>
      <script src="javscript/lib/jquery.bgiframe.js" type="text/javascript"></script>
      <script src="javascript/lib/jquery.dimensions.js" type="text/javascript"></script>
      <script src="javascript/jquery.tooltip.js" type="text/javascript"></script>

      <script type="text/javascript">
      $(function() {
          $('.subject').tooltip({ 
              track: true, 
              delay: 0, 
              showURL: false, 
              bodyHandler: function() { return "Subject";}, 
              fade: 250 
          });

          $('.indirect_object').tooltip({ 
              track: true, 
              delay: 0, 
              showURL: false, 
              bodyHandler: function() { return "Indirect object";}, 
              fade: 250 
          });

          $('.direct_object').tooltip({ 
              track: true, 
              delay: 0, 
              showURL: false, 
              bodyHandler: function() { return "Direct object";}, 
              fade: 250 
          });
      });
      </script>
    </head>

    <body>
    <h1> DIALOGS parser</h1>
"""


utterances=["The bottle is on the table. The bottle is blue. the bottle is Blue", \
    "Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon.", \
    "It's on the table. I give it to you. give me the bottle. I don't give the bottle to you.", \
    "you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?", \
    "You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go", \
    "Isn't he doing his homework and his game now? Can't he take this bottle. good afternoon", \
    "Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema.", \
    "the man, who talks, has a new car. I play the guitar, that I bought yesterday,.", \
    "don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left", \
    "The bottle that I bought from the store which is in the shopping center, , is yours.", \
    "When won't the planning session take place? when must you take the bus", \
    "Where is Broyen ? where are you going. Where must Jido and you be from?", \
    "What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna the Laas?", \
    "what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow", \
    "What's happening. What must happen in the company today? What didn't happen here. no. Sorry.", \
    "What is the biggest bottle's color on your left. What does your brother do for a living?", \
    "What type of people don't read this magazine? what kind of music must he listen to everyday", \
    "What kind of sport is your favorite? what is the problem with him? what is the matter with this person", \
    "How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?", \
    "how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?", \
    "how much water should they transport? how many guests weren't at the party? how much does the motocycle cost", \
    "How about going to the cinema? how have not they gotten a loan for their business? OK", \
    "How did you like Steven Spilburg's new movie. how could I get to the restaurant from here", \
    "Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these.", \
    "What are you thinking about the idea that I present you? what color is the bottle that you bought,", \
    "Which salesperson's competition won the award which we won in the last years", \
    "what'll your house look like? what do you think of the latest novel which Jido wrote", \
    "learn that I want you to give me the blue bottle,. If you do your job, you will be happy.", \
    "what is wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago.", \
    "this is a bottle. There is a bottle on the table", \
    "What do you do for a living in this building? What does your brother do for a living here", \
    "To whom are you talking? you should have the bottle. would you have played a guitar. you would have played a guitar", \
    "you'd like the blue bottle or the glass? the green or blue bottle is on the table. the green or the blue glass is mine?", \
    "learn that I want you to give me the blue bottle that is blue.", \
    "The bottle is behind to me. The bottle is next to the table in front of the kitchen.", \
    "Take the bottle carefully. I take that bottle that I drink in. I take twenty two bottles.", \
    "I'll play Jido's guitar, a saxophone, a piano of the wife of my oncle and Patrick's violon.", \
    "Give me two or three bottles. the bottle is blue, big and fanny. give me the bottle on the table", \
    "the boys' ball is blue. He ask me to do something. is any person courageous on the laboratory", \
    "What must be happened in the company today? The building shouldn't be built fastly. You can be here.", \
    "what size is the best one? What object is blue? How good is this", \
    "Patrick, the bottle is on the table. give it to me", \
    "Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle", \
    "The bottle is not blue but it is red. It is not the glass but the bottle. it is blue or red", \
    "It is not red but blue. this is my banana. bananas are fruits.", \
    "there are no bananas. All bananas are here. give me more information about the bottle.", \
    "Jido, tell me where you go. Goodbye. Bye. there is nothing. it is another one.", \
    "The bottle becomes blue. One piece could become two, if you smoldered it.", \
    "This one is not the bottle of my uncle but it is the bottle of my brother. It is not on the table but on the shelf.", \
    "Give me the fourth and seventh bottle. Give me the one thousand ninth and the thirty thousand twenty eighth bottle.", \
    "the evil tyrant is in the laboratory. I don't know what are you talking about.", \
    "I go to the place where I was born. I study where you studied. I study where you build your house where you put the bottle.", \
    "apples grow on trees and plants. give me three apples.", \
    "When your father came, we was preparing the dinner. While I phoned, he made a sandwich with bacons.", \
    "the big and very strong man is on the corner. the too big and very strong man is on the corner.", \
    "red apples grow on green trees and plants. a kind of thing. It can be played by thirty thousand twenty eight players.", \
    "let the man go to the cinema. Is it the time to let you go. And where is the other tape.", \
    "And now, can you reach the tape. it could have been them. It is just me at the door. A strong clause can stand on its own", \
    "tell me what to do. No, I can not reach it.", \
    "I will come back on monday. I'll play with guitar. I'll play football", \
    "I'll play guitar, piano and violon. I'll play with guitar, piano and violon. give me everything", \
    "I will come back at seven o'clock tomorrow. He finish the project 10 minutes before.", \
    "I'll play a guitar a piano and a violon. I'll play with a guitar a piano and a violon. the boss you and me are here", \
    "The time of speaking sentence is the best. I come at 10pm. I will come tomorrow evening", \
    "I think that I know who is he. see you. So I want to go", \
    "the interpretation is to find a defenition or a rule for something. and in a dialog, there is an interaction between them", \
    "To have a dialog, we need more than 1 protagonist. I finish the dialog, and I check many problems", \
    "the left of what? Jido, what do you do? throw one of them. Very good", \
    "the bottle on the table, is blue. where is this tape", \
    "the bottle of Jido which is blue, is on the table. I do my homework before he comes", \
    "before he comes, I do my homework. I have played foot since I was a young boy.", \
    "They haven't played tennis since 1987. give me the glass the paper and the bottle."]


for s in utterances:
    preprocessed = parser.preprocess(s, None)
    parsed = parser.parse(preprocessed, None)
    print("<h2>" + s + "</h2>")
    for p in parsed:
        print(str(p))


print """
    </body>
</html>
"""


