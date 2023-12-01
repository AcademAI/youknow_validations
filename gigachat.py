"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

class GigaChat_impl:
    def __init__(self, credentials, scope, verify_ssl_certs):
        self.credentials = credentials
        self.scope = scope
        self.verify_ssl_certs = verify_ssl_certs
        self.giga = GigaChat(credentials=self.credentials, scope=self.scope, verify_ssl_certs=self.verify_ssl_certs)

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
        print(format_instructions)

        template_string = """Ты - помощник, способный курировать содержание курса, придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы. \
        You come up with catchy and memorable brand names.

        Take the brand description below delimited by triple backticks and use it to create the name for a brand. 

        brand description: ```{brand_description}```

        then based on the description and you hot new brand name give the brand a score 1-10 for how likely it is to succeed. В ответе верни массив, состоящий из JSON объектов глав.

        {format_instructions}
        """

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
        
