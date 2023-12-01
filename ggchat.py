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
        print(len(units))

        # Define the ResponseSchema for the chapters
        #units_schema = ResponseSchema(name='title', description='название раздела', type='string')
        chapters_schema1 = ResponseSchema(name='chapters1', description='3 главы 1-го раздела', type='List[{youtube_search_query: string, chapter_title: string}]')
        chapters_schema2 = ResponseSchema(name='chapters2', description='3 главы 2-го раздела', type='List[{youtube_search_query: string, chapter_title: string}]')
        chapters_schema3 = ResponseSchema(name='chapters3', description='3 главы 3-го раздела', type='List[{youtube_search_query: string, chapter_title: string}]')

        response_schemas = [#units_schema,
                            chapters_schema1,
                            chapters_schema2,
                            chapters_schema3
                            ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        print(format_instructions)

        template_string = """Ты - помощник, способный курировать содержание курса. \
        Ты можешь придумывать соответствующие названия глав и придумывать поисковые запросы youtube для каждоый главы

        Твоя задача - создать курс о ```{title}``` 
        У тебя есть разделы курса ```{units}``` , тебе нужно сгенерировать для каждого раздела 3 новые главы на отдельные подтемы
        Затем для каждой главы сгенерируй поисковый запрос в youtube_search_query и название chapter_title.

        {format_instructions}
        """
        prompt = ChatPromptTemplate.from_template(template=template_string)

        messages = prompt.format_messages(title=title, 
                                            units=units,
                                            unitsLength=len(units),
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
