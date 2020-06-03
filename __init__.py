from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.core import MycroftSkill, intent_handler


class HospitalAssistant(MycroftSkill):
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
        self.temp = float(message.data.get('utterance'))
        if self.temp < 37.0:
            self.speak("la temperatura va bene")
        elif self.temp >= 37.0 and self.temp <= 38.0:
            self.speak("Non è molto alta, ma è meglio tenerla sotto controllo. Misurala più di una volta al giorno")
        elif self.temp > 38.0:
            self.speak("La temperatura è alta!")
        
        self.speak_dialog('otherdays', expect_response=True)

    @intent_handler(IntentBuilder('').require("daysbefore").require("TempContext").build())
    @adds_context("DaysB4")
    def handle_final_intent(self, message):
        before = message.data.get('utterance')
        if 'uguale' in before and self.temp < 37.0:
            self.speak("Ottimo, la tua temperatura è stata sempre ok.")
        elif 'uguale' in before and self.temp >= 37.0:
            self.medicine = True 
            self.speak("Se non è dimunita nemmeno dopo diversi giorni potrebbe esserci qualcosa che non va")
        elif 'alta' in before and self.temp > 35.0 and self.temp < 39.0:
            self.speak("La temperatura è diminuita, è già un buon segno")
        elif 'alta' in before and self.temp > 38.0:
            self.speak("La temperatura è diminuita ma non abbastanza, continua a monitorarla")
        elif 'bassa' in before and self.temp > 37.0:
            self.speak("La temperatura è aumentata, potrebbe esserci un problema")
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
        if self.temp <= 37.0:
            self.speak("Dato che la temperatura è bassa i tuoi problemi respiratòri potrebbero derivare da questo, non da altri problemi. Prenota una visita per sicurezza")
            self.speak_dialog('bye')
        elif self.temp > 37.0:
            self.speak("è un fattore importante da non trascurare, i tuoi problemi respiratòri potrebbero essere legati a quello, ma la tua temperatura è alta. Meglio se prenoti una visita")
            self.speak_dialog('bye')
    # NO ASMA 
    @intent_handler(IntentBuilder('').require("nokey").require("SiProblems").build())
    def handle_no_asma_intent(self, message):
        if self.temp < 38.0:
            self.speak("I tuoi problemi respiratòri potrebbero avere diverse cause, l'assenza di febbre però è un buon segno. prenota una visita medica per sicurezza")
            self.speak_dialog('bye')
        elif self.temp >= 38.0:
            self.speak("La temperatura alta con problemi respiratòri non è un buon segno, fai una visita il prima possibile")
            self.speak_dialog('bye')
    
    @intent_handler(IntentBuilder('').require("nokey").require("DaysB4").build())
    def handle_no_problems_respiratori_intent(self, message):
        if self.temp < 38.0:
            self.speak("Allora non c'è nulla di cui preoccuparsi, resta solo un pò a riposo")
            self.speak_dialog('bye')
        elif self.temp >= 38.0:
            self.speak("La febbre è alta ma l'assenza di problemi respiratòri è un buon segno, monitora la tua febbre, se non diminuisce contatta il dottore")
            self.speak_dialog('bye')

    # FEBBRE NON MISURATA, NO PROBLEMI RESPIRATORI
    @intent_handler(IntentBuilder('').require('nokey').require("NoMisurata").build())
    def handle_no_tosse_intent(self, message):
        self.speak("è già un buon segno, misura la febbre, se vedi che è alta richiama!")
        self.speak_dialog('bye')
    
    # FEBBRE NON MISURATA, Si PROBLEMI RESPIRATORI
    @intent_handler(IntentBuilder('').require("yeskey").require("NoMisurata").build())
    
    def handle_si_tosse_intent(self, message):
        self.speak("misura subito la febbre, se noti che la febbre è alta prenota subito una visita dal dottore")
        self.speak_dialog('bye')
    

def create_skill():
    return HospitalAssistant()