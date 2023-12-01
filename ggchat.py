"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import json

class GigaChat_impl:
    def __init__(self, credentials, scope, verify_ssl_certs):
        
        self.giga = GigaChat(credentials=credentials, scope=scope, verify_ssl_certs=verify_ssl_certs)

    async def createUnitsNChapters(self, title, units):
        #SYSTEM "Ты - помощник, способный курировать содержание курса, придумывать соответствующие названия глав и находить подходящие видеоролики на youtube для каждой главы. В ответе верни массив, состоящий из JSON объектов глав."
        print(title)
        print(units)
        units_list = units.split(",")
        print(len(units_list))

        response_schemas = []

        # Define the ResponseSchema for the chapters
        #units_schema = ResponseSchema(name='title', description='название раздела', type='string')
        for i, unit in enumerate(units_list, start=1):
            chapters_schema = ResponseSchema(name=f'chapters{i}', description=f'3 главы {i}-го раздела', type='List[{youtube_search_query: string, chapter_title: string}]')
            response_schemas.append(chapters_schema)

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
        
        response = self.giga(messages)
        response_as_dict = output_parser.parse(response.content)
        print(response_as_dict)

        units_list = units.split(",")

        result = []

        print(response_as_dict)

        units_list = units.split(",")

        # Get the chapters from the response_as_dict
        chapters_list = list(response_as_dict.values())

        # Map the units to the chapters by order
        result = [{"title": unit, "chapters": chapters} for unit, chapters in zip(units_list, chapters_list)]

        # Convert the result to JSON
        result_json = json.dumps(result, indent=4)

        print(result_json)

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
        
