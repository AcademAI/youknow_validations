"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

class GigaChat_impl:
    def __init__(self, credentials, scope, verify_ssl_certs):
        
        self.giga = GigaChat(credentials=credentials, scope=scope, verify_ssl_certs=verify_ssl_certs)

    async def createUnitsNChapters(self, title, units):
        #SYSTEM "Ты - помощник, способный курировать содержание курса, придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы. В ответе верни массив, состоящий из JSON объектов глав."
        print(title)
        print(units)

        # Define the ResponseSchema for the title


        # Define the ResponseSchema for the chapter
        #chapter_schema = ResponseSchema(name='chapter', description='A chapter in the course', type='string')

        # Define the ResponseSchema for the chapters
        chapters_schema = ResponseSchema(name='chapters', description='The chapters of the course', type='List[Chapter]')

        response_schemas = [#,
                            chapters_schema,
                            ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        print(format_instructions)

        template_string = """Ты - помощник, способный курировать содержание курса. \
        Ты можешь придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы

        Твоя задача - создать курс о ```{title}``` 
        Сгенерируй главы под каждый раздел: ```{units}``` 
        Затем для каждой главы сгенерируй поисковый запрос в youtube и название главы.

        {format_instructions}
        """
        prompt = ChatPromptTemplate.from_template(template=template_string)

        messages = prompt.format_messages(title=title, 
                                            units=units,
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
        

    async def call_gigachat(self, action, title, units):
        if action == 'createUnitsNChapters':
            return await self.createUnitsNChapters(title, units)
        elif action == 'createKandinskyPrompt':
            return await self.createKandinskyPrompt()
        
