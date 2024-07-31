

class ParserCallback:
    def on_start_save(self, instance):
        """
        Called when the parser has started saving
        """
        pass
    def on_finish_init(self, instance):
        """
        Called when the parser has finished initializing
        """
        pass

    def on_start_convert(self, instance):
        """
        Called when the parser has started converting
        """
        pass

    def on_finish_convert(self, instance):
        """
        Called when the parser has finished converting
        """
        pass

    def on_start_translate(self, instance):
        """
        Called when the parser has started translating
        """
        pass

    def on_finish_translate(self, instance):
        """
        Called when the parser has finished translating
        """
        pass

    def on_error_translate(self, instance, error):
        """
        Called when the parser has encountered an error during translation
        """
        pass


class VerboseCallback(ParserCallback):
    def on_start_save(self, instance):
        print(f"Parser {instance.parser_name} has started saving")
    
    def on_finish_save(self, instance):
        print(f"Parser {instance.parser_name} has finished saving")

    def on_finish_init(self, instance):
        print(f"Parser {instance.parser_name} has finished initializing")

    def on_start_convert(self, instance):
        print(f"Parser {instance.parser_name} has started converting")

    def on_finish_convert(self, instance):
        print(f"Parser {instance.parser_name} has finished converting")

    def on_start_translate(self, instance):
        print(f"Parser {instance.parser_name} has started translating")

    def on_finish_translate(self, instance):
        print(f"Parser {instance.parser_name} has finished translating")

    def on_error_translate(self, instance, error):
        print(f"Parser {instance.parser_name} has encountered an error during translation")
        print(error)
