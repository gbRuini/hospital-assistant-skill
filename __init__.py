from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, remove_context
from mycroft import intent_handler, 
from mycroft.skills.core import MycroftSkill, intent_file_handler


class HospitalAssistant(MycroftSkill):
    
    @intent_handler(IntentBuilder("").require("TeaKeyword"))
    def handle_crystalball_intent(self, message):
    	self.answer()

    def answer(self):
        # Mycroft responds with a random yes/no answer
        self.speak_dialog("answer")

    """
    @intent_handler(IntentBuilder('TeaIntent').require("TeaKeyword"))
    @adds_context('MilkContext')
    def handle_tea_intent(self, message):
        self.milk = False
        self.speak('Certo,vuoi anche del latte?', expect_response=True)
    @intent_handler(IntentBuilder('NoMilkIntent').require("NoKeyword").require('MilkContext').build())
    @removes_context('MilkContext')
    @adds_context('HoneyContext')
    def handle_no_milk_intent(self, message):
        self.speak('va bene, del miele?', expect_response=True)
    
    @intent_handler(IntentBuilder('YesMilkIntent').require("YesKeyword").require('MilkContext').build())
    @removes_context('MilkContext')
    @adds_context('HoneyContext')
    def handle_yes_milk_intent(self, message):
        self.milk = True
        self.speak('Anche del miele?', expect_response=True)
    @intent_handler(IntentBuilder('NoHoneyIntent').require("NoKeyword").require('HoneyContext').build())
    @removes_context('HoneyContext')
    def handle_no_honey_intent(self, message):
        if self.milk:
            self.speak('Ecco il tuo tè con il latte')
        else:
            self.speak('Ecco a te il tè')
    @intent_handler(IntentBuilder('YesHoneyIntent').require("YesKeyword").require('HoneyContext').build())
    @removes_context('HoneyContext')
    def handle_yes_honey_intent(self, message):
        if self.milk:
            self.speak('Ecco il tuo tè con latte e miele')
        else:
            self.speak('Ecco il te con il miele')
    
   
    
    def initialize(self):
        self.register_intent_file('ti.piacciono.intent', self.handle_ti_piacciono)
   
    @intent_file_handler('assistant.hospital.intent')
    def handle_assistant_hospital(self, message):
        self.speak_dialog('hai.misurato.la.febbre?')

    @intent_file_handler('ti.piacciono.intent')
    def handle_ti_piacciono(self, message):
        tipo_pomodoro = message.data.get('type')
        if tipo_pomodoro is not None:
            self.speak_dialog('mi.piacciono.type', {'type': tipo_pomodoro})
        else:
            self.speak_dialog('mi.piacciono.tutti')
    """
    

def create_skill():
    return HospitalAssistant()

