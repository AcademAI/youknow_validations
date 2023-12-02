"""Пример работы с чатом через gigachain"""

from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import tenacity
from tenacity import retry, stop_after_attempt, wait_fixed

import json

class GigaChat_impl:
    def __init__(self, credentials, scope, verify_ssl_certs):
        
        self.giga = GigaChat(credentials=credentials, scope=scope, verify_ssl_certs=verify_ssl_certs)

    async def createUnitsNChapters(self, title, units):
        units_list = units.split(",")
        response_schemas = []

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
        result = []

        # Get the chapters from the response_as_dict
        chapters_list = list(response_as_dict.values())

        # Map the units to the chapters by order
        result = [{"title": unit, "chapters": chapters} for unit, chapters in zip(units_list, chapters_list)]

        # Convert the result to JSON
        result_json = json.dumps(result, indent=4)

        return result_json

        # What we get here
        """[
            { title: 'functions', chapters: [ [Object], [Object], [Object] ] },
            { title: 'classes', chapters: [ [Object], [Object], [Object] ] },
            { title: 'decorators', chapters: [ [Object], [Object], [Object] ] }
        ]"""

    
    async def createImageSearchTerm(self, title):
        response_schemas = []
        chapters_schema = ResponseSchema(name=f'image_search_term', description=f'a good prompt for course thumbnail generation', type='{image_search_term: string}')
        response_schemas.append(chapters_schema)

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        print(format_instructions)

        template_string = """You are an assistant capable of evaluating the best prompt for course thumbnail generation. \
        Please provide a good prompt for midjourney to generate a good image about: ```{title}``` 

        Return a JSON object with only 1 key and 1 value, nothing else.

        {format_instructions}
        """
        prompt = ChatPromptTemplate.from_template(template=template_string)
        messages = prompt.format_messages(title=title, 
                                            format_instructions=format_instructions)
        
        response = self.giga(messages)
        response_as_dict = output_parser.parse(response.content)
        print(response_as_dict)

        # Convert the result to JSON
        result_json = json.dumps(response_as_dict, indent=4)

        return result_json

        # What we get here
        """[ { image_search_term: 'a good search term for the title of the course' } ]"""
        


    async def call_gigachat(self, action, title, units):
        if action == 'createUnitsNChapters':
            return await self.createUnitsNChapters(title, units)
        elif action == 'createImageSearchTerm':
            return await self.createImageSearchTerm(title)
        
