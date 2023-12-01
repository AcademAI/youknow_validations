"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

class GigaChat_impl:
    def __init__(self, credentials, scope, verify_ssl_certs):
        
        self.giga = GigaChat(credentials=credentials, scope=scope, verify_ssl_certs=verify_ssl_certs)

    async def createUnitsNChapters(self, user_prompt):
        #SYSTEM "Ты - помощник, способный курировать содержание курса, придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы. В ответе верни массив, состоящий из JSON объектов глав."
        print(user_prompt)

        """title = ResponseSchema(name="title",
                                description="Название раздела")"""

        chapter_title_schema = ResponseSchema(name="chapter_title",
                                            description="Название главы")

        youtube_search_query_schema = ResponseSchema(name="youtube_search_query",
                                                    description="youtube_search_query для поиска видео")

        response_schemas = [#title, 
                            chapter_title_schema,
                            youtube_search_query_schema
                            ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        #print(format_instructions)

        template_string = """Ты - помощник, способный курировать содержание курса. \
        Ты можешь придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы

        Возьми название курса. 

        course name: ```{user_prompt}```

        then based on the description and you hot new brand name give the brand a score 1-10 for how likely it is to succeed. В ответе верни массив, состоящий из JSON объектов глав.

        {format_instructions}
        """
        prompt = ChatPromptTemplate.from_template(template=template_string)

        messages = prompt.format_messages(user_prompt=user_prompt, 
                                        format_instructions=format_instructions)

        #print(messages[0].content)

        
        response = self.giga(messages)
        response_as_dict = output_parser.parse(response.content)
        print(response_as_dict)
    
        

        # WHAT WE WANT TO GET
        """[
            { title: 'functions', chapters: [ [Object], [Object], [Object] ] },
            { title: 'classes', chapters: [ [Object], [Object], [Object] ] },
            { title: 'decorators', chapters: [ [Object], [Object], [Object] ] }
        ]"""

        # OUTPUT FORMAT
        """{
        title: "название раздела",
        chapters:
          "массив глав, каждая глава должна иметь youtube_search_query и ключ chapter_title в JSON-объекте",
        }
        # WHAT TYPESCRIPT AWAITS
        type outputUnits = {
        title: string;
        chapters: {
            youtube_search_query: string;
            chapter_title: string;
        }[];
        }[];
        
        """

    async def createKandinskyPrompt(self):
        # "Ты - помощник, способный курировать содержание курса, придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы. В ответе верни массив, состоящий из JSON объектов глав."
        
        pass
        

    async def call_gigachat(self, action, user_prompt):
        if action == 'createUnitsNChapters':
            return await self.createUnitsNChapters(user_prompt)
        elif action == 'createKandinskyPrompt':
            return await self.createKandinskyPrompt()
        
