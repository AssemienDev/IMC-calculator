from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivymd.uix.toolbar import MDTopAppBar

KV = '''


<CommonComponentInfo>
    font_size: "25sp"

<CommonComponentSaisie_taille>
    pos_hint:{ "center_x":.5, "center_y": .66}
    size_hint_x: .5
    max_text_length: 3
    size_hint_y: .125
    font_size: "26sp"
    hint_text_color_normal:"purple"
    hint_text_color_focus:"purple"
    line_color_focus: "purple"


<CommonComponentSaisie_poids>
    pos_hint:{ "center_x":.5, "center_y": .52}
    size_hint_x: .5
    size_hint_y: .125
    max_text_length: 5
    font_size: "26sp"
    hint_text_color_normal:"purple"
    hint_text_color_focus:"purple"
    line_color_focus: "purple"

<CommonComponentbouton>
    pos_hint:{ "center_x":.5, "center_y": .39}
    size_hint_x: .5
    md_bg_color:"purple"
    on_release: app.root.show_alert_dialog()


<MobileView>

    CommonComponentInfo:
        text:"Le Calculateur d'IMC(Indice de Masse Corporel):"
        pos_hint:{ "center_x":.55, "center_y": .82}
        font_size: "18sp"

    CommonComponentSaisie_taille:
        hint_text:"entrer votre taille:"
        hint_text_color:"purple"
        

    CommonComponentSaisie_poids:
        hint_text:"entrer votre poids:"
        hint_text_color:"purple"


    CommonComponentBouton:
        text: "Calculer"



<TabletView>
    MDBottomAppBar:
        md_bg_color:"purple"
        MDTopAppBar:
            title:'Bienvenue'
            icon:"account"
            icon_color:"purple"
            mode:'end'
            type:'bottom'
            left_action_items:[["menu", lambda x:nav_drawer.set_state("open")]]
        
    
    CommonComponentInfo:
        text:"Le Calculateur d'IMC(Indice de Masse Corporel):"
        pos_hint:{ "center_x":.68, "center_y": .82}

    CommonComponentSaisie_taille:
        hint_text:"entrer votre taille:"

    CommonComponentSaisie_poids:
        hint_text:"entrer votre poids:"

    CommonComponentBouton:
        text: "Calculer"
        
    MDNavigationDrawer:
        id:nav_drawer
        radius: (0,16,16,0)
        md_bg_color:"white"
        
        MDNavigationDrawerHeader:
            title:'Page Action'
            pos_hint:{ "center_x":.4, "center_y": .95}
            
            
        

<DesktopView>

    CommonComponentInfo:
        text:"Le Calculateur d'IMC(Indice de Masse Corporal):"
        pos_hint:{ "center_x":.8, "center_y": .82}

    CommonComponentSaisie_taille:
        hint_text:"entrer votre taille:"

    CommonComponentSaisie_poids:
        hint_text:"entrer votre poids:"

    CommonComponentBouton:
        text: "Calculer"

<HomeResponsiveView>:
    name:'homepage'

WindowManager:
    HomeResponsiveView:
'''


class CommonComponentInfo(MDLabel):
    pass


class CommonComponentSaisie_taille(MDTextField):
    pass


class CommonComponentSaisie_poids(MDTextField):
    pass


class CommonComponentBouton(MDRaisedButton):
    pass


class MobileView(MDScreen):
    pass


class TabletView(MDScreen):
    pass


class DesktopView(MDScreen):
    pass


class HomeResponsiveView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
        self.dialog = None
        Clock.schedule_once(self.show_author, 0.5)


    def show_author(self, interval):
        Snackbar(
            text="By Monster Black",
            snackbar_x="340dp",
            snackbar_y="5dp",
            size_hint_x=.18,
            size_hint_y=.07,
            bg_color=(0.5,0,0.5,1)
        ).open()

    def calcul_imc(self, poids, taille):
        taille_metre = taille / 100.0
        imc = poids / (taille_metre ** 2)
        return imc

    def show_alert_dialog(self):
        self.dialog = None

        if self.tablet_view:
            try:
                poids = float(self.tablet_view.children[1].text)
            except ValueError:
                poids = self.tablet_view.children[1].text
            try:
                taille = int(self.tablet_view.children[2].text)
            except ValueError:
                taille = self.tablet_view.children[2].text
            if type(taille) == int and type(poids) == float:
                saisie = self.calcul_imc(float(poids), float(taille))
                if saisie < 18.5:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Insuffisance pondérale(maigreur)".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 18.5 <= saisie < 25:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Corpulence normale".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 25.0 <= saisie < 30.0:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Surpoids".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 30.0 <= saisie < 35.0:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            text="{:.2f}: Obésité modérée".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 35 <= saisie < 40:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Obésité sévère".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif saisie > 40:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Obésité morbide".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()

            elif type(taille) != int:
                # Activer le focus sur le champ de taille
                self.tablet_view.children[2].focus = True
                self.tablet_view.children[2].line_color_focus = "red"
                self.tablet_view.children[2].helper_text_mode = "persistent"
                self.tablet_view.children[2].helper_text_color_focus = "red"
                self.tablet_view.children[2].helper_text = "Uniquement des chiffres"

            elif type(poids) != float:
                # Activer le focus sur le champ de poids
                self.tablet_view.children[1].focus = True
                self.tablet_view.children[1].line_color_focus = "red"
                self.tablet_view.children[1].helper_text_mode = "persistent"
                self.tablet_view.children[1].helper_text_color_focus = "red"
                self.tablet_view.children[1].helper_text = "Uniquement des chiffres"

        # pour mobile
        if self.mobile_view:
            try:
                poids1 = float(self.mobile_view.children[1].text)
            except ValueError:
                poids1 = self.mobile_view.children[1].text
            try:
                taille1 = int(self.mobile_view.children[2].text)
            except ValueError:
                taille1 = self.mobile_view.children[2].text
            if type(taille1) == int and type(poids1) == float:
                saisie = self.calcul_imc(float(poids1), float(taille1))
                if saisie < 18.5:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Insuffisance pondérale(maigreur)".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 18.5 <= saisie < 25:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Corpulence normale".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 25.0 <= saisie < 30.0:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Surpoids".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 30.0 <= saisie < 35.0:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            text="{:.2f}: Obésité modérée".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif 35 <= saisie < 40:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Obésité sévère".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()
                elif saisie > 40:
                    if self.dialog is None:
                        self.dialog = MDDialog(
                            title='Votre IMC est:',
                            radius=[20, 7, 20, 7],
                            text="{:.2f}: Obésité morbide".format(saisie),
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    text_color="blue",
                                    on_release=lambda *args: self.dialog.dismiss()),
                            ],
                        )
                        self.dialog.open()

            elif type(taille1) != int:
                # Activer le focus sur le champ de taille
                self.mobile_view.children[2].focus = True
                self.mobile_view.children[2].line_color_focus = "red"
                self.mobile_view.children[2].helper_text_mode = "persistent"
                self.mobile_view.children[2].helper_text_color_focus = "red"
                self.mobile_view.children[2].helper_text = "Uniquement des chiffres"

            elif type(poids1) != float:
                # Activer le focus sur le champ de poids
                self.mobile_view.children[1].focus = True
                self.mobile_view.children[1].line_color_focus = "red"
                self.mobile_view.children[1].helper_text_mode = "persistent"
                self.mobile_view.children[1].helper_text_color_focus = "red"
                self.mobile_view.children[1].helper_text = "Uniquement des chiffres"


class WindowManager(ScreenManager):
    def show_alert_dialog(self):
        current_screen = self.current_screen
        if isinstance(current_screen, HomeResponsiveView) and current_screen.tablet_view:
            current_screen.show_alert_dialog()
        elif isinstance(current_screen, HomeResponsiveView) and current_screen.desktop_view:
            current_screen.show_alert_dialog()
        elif isinstance(current_screen, HomeResponsiveView) and current_screen.mobile_view:
            current_screen.show_alert_dialog()


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

Test().run()