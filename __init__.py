from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.core import MycroftSkill, intent_handler


class Prova(MycroftSkill):
    @intent_handler(IntentBuilder("").require("sick"))
    @adds_context("Febbre")
    def handle_fever_intent(self, message):
        self.speak_dialog('welcome', expect_response=True)
        
    # FEBBRE NON E' STATA MISURATA
    @intent_handler(IntentBuilder('').require('nokey').require("Febbre").build())
    @adds_context("NoMisurata")
    def handle_no_fever_intent(self, message):
        self.speak_dialog('advicetemp') 
        self.speak("Hai problemi respiratòri?", expect_response=True)
    
    # febbre è stata misurata
    @intent_handler(IntentBuilder('').require('yeskey').require("Febbre").build())
    @adds_context("SiMisurata")
    def handle_yes_fever_intent(self, message):
        self.speak("Quant'era?", expect_response=True)
    
    @intent_handler(IntentBuilder('').require('temp').require("SiMisurata").build())
    @adds_context("TempContext")
    def handle_temp_intent(self, message):
        self.temp = int(message.data.get('utterance'))
        if self.temp < 37:
            self.speak("la temperatura va bene")
        elif self.temp == 37 or self.temp == 38:
            self.speak("Non è molto alta, ma è meglio tenerla sotto controllo. Misurala più di una volta al giorno")
        elif self.temp > 38:
            self.speak("La temperatura è alta!")
        
        self.speak_dialog('otherdays', expect_response=True)

    @intent_handler(IntentBuilder('').require("daysbefore").require("TempContext").build())
    @adds_context("DaysB4")
    def handle_final_intent(self, message):
        before = message.data.get('utterance')
        if 'uguale' in before and self.temp < 37:
            self.speak_dialog("Allora è tutto ok")
        elif 'uguale' in before and self.temp >= 37:
            self.medicine = True 
            self.speak("Se non è dimunita nemmeno dopo diversi giorni potrebbe esserci un problema", expect_response=True)
        elif 'alta' in before and self.temp > 35:
            self.speak_dialog("La temperatura è diminuita, è già un buon segno")
        elif 'bassa' in before and self.temp > 37:
            self.speak_dialog("La temperatura è aumentata, potrebbe esserci un problema")
        self.remove_context('SiMisurata')
        self.remove_context('TempContext')
        self.speak_dialog("Hai anche problemi respiratòri?", expect_response=True)
            

    @intent_handler(IntentBuilder('').require("yeskey").require("DaysB4").build())
    @adds_context("SiProblems")
    # GESTISCO SI PROBLEMI RESPIRATORI CON FEBBRE
    def handle_yes_problems_respiratori_intent(self, message):
        self.speak_dialog("Soffri d'asma?", expect_response=True)

    # SI ASMA 
    @intent_handler(IntentBuilder('').require("yeskey").require("SiProblems").build())
    def handle_yes_asma_intent(self, message):
        if self.temp <= 37:
            self.speak("Dato che la temperatura è bassa allora potrebbe essere causato dall'asma, se vedi che non passa prenota una visita")
        elif self.temp > 37:
            self.speak("è un fattore importante da non trascurare, prenota una visita per sicurezza")
    # NO ASMA 
    @intent_handler(IntentBuilder('').require("nokey").require("SiProblems").build())
    def handle_no_asma_intent(self, message):
        if self.temp < 38:
            self.speak("Sono sicuro che non è niente di grave, ma prenota una visita medica per sicurezza")
        elif self.temp >= 38:
            self.speak("Potrebbe esserci qualche problema, fai una visita il prima possibile")
    
    @intent_handler(IntentBuilder('').require("nokey").require("DaysB4").build())
    def handle_no_problems_respiratori_intent(self, message):
        if self.temp < 38:
            self.speak("Allora non c'è nulla di cui preoccuparsi, resta solo un pò a riposo")
        elif self.temp >= 38:
            self.speak("La febbre è alta ma l'assenza di problemi respiratori è un buon segno, monitora la tua febbre, se non diminuisce contatta il dottore")

    # FEBBRE NON MISURATA, NO PROBLEMI RESPIRATORI
    @intent_handler(IntentBuilder('').require('nokey').require("NoMisurata").build())
    def handle_no_tosse_intent(self, message):
        self.speak_dialog("è già un buon segno, misura la febbre, se vedi che è alta richiama! Buona giornata")
    
    # FEBBRE NON MISURATA, Si PROBLEMI RESPIRATORI
    @intent_handler(IntentBuilder('').require("yeskey").require("NoMisurata").build())
    
    def handle_si_tosse_intent(self, message):
        self.speak("misura subito la febbre, se noti che la febbre è alta prenota subito una visita dal dottore")
    

def create_skill():
    return Prova()