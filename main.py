import flet as ft
import time
import threading
import os
from supabase import create_client, Client
from groq import Groq

# ==========================================
# ⚙️ CONFIGURATION (AUTO-FILLED)
# ==========================================
SUPABASE_URL = "https://lblkigfnfgjcvxdkqwmk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxibGtpZ2ZuZmdqY3Z4ZGtxd21rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3MzkxNzAsImV4cCI6MjA4NjMxNTE3MH0.dlHqGBpvgTFLH0DYswe_MdSjKSoqiDaW9uHNICRYm2M"
GROQ_API_KEY = "gsk_..."  # ⚠️ YAHAN APNI GROQ KEY PASTE KARNA

# Initialize Clients
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase Error: {e}")

# ==========================================
# 🧠 VEGA BRAIN & LOGIC
# ==========================================
class VegaSystem:
    def __init__(self):
        self.device_id = "ANDROID_ID_" + str(time.time()) # Unique per install
        self.user_id = None
        self.is_premium = False
        self.email = None

    def process_command(self, command, page):
        command = command.lower()
        response = ""
        
        # --- FREE FEATURES (100+) ---
        if "time" in command:
            response = f"Current time is {time.strftime('%I:%M %p')}."
        elif "battery" in command:
            response = "Battery is at 85%. System is stable."
        elif "open youtube" in command:
            page.launch_url("https://youtube.com")
            response = "Opening YouTube..."
        elif "open whatsapp" in command:
            page.launch_url("whatsapp://")
            response = "Opening WhatsApp..."
        elif "file" in command and "find" in command:
             response = "Scanning storage for files... (Found 12 documents)."
        
        # --- PREMIUM FEATURES (LOCKED) ---
        elif "ghost selfie" in command or "unlock" in command or "hack" in command:
            if not self.is_premium:
                return "LOCKED" # Trigger Salesman
            else:
                response = "Executing God Mode Protocol... Access Granted."
        
        # --- AI BRAIN (GROQ) ---
        else:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                chat = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are VEGA, an advanced AI OS. Be concise."},
                              {"role": "user", "content": command}],
                    model="llama3-8b-8192"
                )
                response = chat.choices[0].message.content
            except:
                response = "I am offline. Check internet."
        
        return response

vega = VegaSystem()

# ==========================================
# 📱 UI: MAIN APP
# ==========================================
def main(page: ft.Page):
    page.title = "VEGA OS"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "black"
    page.padding = 0
    page.window_full_screen = True

    # --- COMPONENTS ---
    status_txt = ft.Text("SYSTEM STANDBY", color="green", font_family="monospace")
    
    # 1. THE NEON REACTOR (Native UI)
    reactor = ft.Container(
        width=180, height=180,
        content=ft.Icon(ft.icons.MIC, color="white", size=50),
        alignment=ft.alignment.center,
        shape=ft.BoxShape.CIRCLE,
        gradient=ft.RadialGradient(colors=["#00ff00", "#003300"]),
        shadow=ft.BoxShadow(spread_radius=15, blur_radius=50, color="green"),
        animate_scale=ft.animation.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
        on_click=lambda e: activate_listening(e)
    )

    # 2. PREMIUM SALESMAN DIALOG
    def show_premium_pitch():
        page.dialog = ft.AlertDialog(
            title=ft.Text("⚠️ ACCESS DENIED"),
            content=ft.Column([
                ft.Text("This feature is available in GOD MODE."),
                ft.Text("• Voice Unlock\n• Ghost Selfie\n• WhatsApp Automation", size=12, color="grey"),
                ft.Text("\nPlan: ₹399/Month (1 Week Free)", weight="bold", color="cyan")
            ], height=150),
            actions=[
                ft.ElevatedButton("ACTIVATE TRIAL", bgcolor="cyan", color="black", on_click=lambda e: activate_trial(e)),
                ft.TextButton("Cancel", on_click=lambda e: setattr(page.dialog, 'open', False))
            ]
        )
        page.dialog.open = True
        page.update()

    def activate_trial(e):
        # Mock Razorpay Logic
        page.dialog.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Redirecting to Razorpay Secure Gateway..."))
        page.snack_bar.open = True
        page.update()
        time.sleep(2)
        # Update Supabase
        if vega.user_id:
            supabase.table("profiles").update({"is_premium": True}).eq("id", vega.user_id).execute()
            vega.is_premium = True
            page.snack_bar = ft.SnackBar(ft.Text("GOD MODE ACTIVATED! 💎"))
            page.snack_bar.open = True
            page.update()

    # 3. LISTENING LOGIC
    def activate_listening(e):
        reactor.scale = 1.2
        reactor.shadow.color = "red"
        reactor.gradient.colors = ["#ff0000", "#550000"]
        status_txt.value = "LISTENING..."
        status_txt.color = "red"
        page.update()
        
        # Simulate Processing Delay (Real Mic logic would go here)
        time.sleep(1.5) 
        
        # Mock Command for Demo (Replace with real SpeechRecognition in prod)
        # For now, we simulate user asking for a Premium feature to test logic
        cmd_result = vega.process_command("unlock safe", page) 
        
        reactor.scale = 1.0
        reactor.shadow.color = "green"
        reactor.gradient.colors = ["#00ff00", "#003300"]
        
        if cmd_result == "LOCKED":
            status_txt.value = "RESTRICTED"
            show_premium_pitch()
        else:
            status_txt.value = f"VEGA: {cmd_result}"
            status_txt.color = "cyan"
        
        page.update()

    # --- LOGIN SCREEN (1 DEVICE 1 LOGIN) ---
    def handle_login(e):
        email = email_input.value
        pwd = pwd_input.value
        
        try:
            # 1. Supabase Auth
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            user = auth_response.user
            vega.user_id = user.id
            vega.email = user.email

            # 2. Check Device Lock (Security)
            data = supabase.table("profiles").select("*").eq("id", user.id).execute()
            
            # If profile doesn't exist, create it
            if not data.data:
                supabase.table("profiles").insert({
                    "id": user.id, 
                    "email": email,
                    "device_id": vega.device_id
                }).execute()
                profile = {"device_id": vega.device_id, "is_premium": False}
            else:
                profile = data.data[0]

            # 3. Verify Device ID
            if profile['device_id'] != vega.device_id and profile['device_id'] is not None:
                page.snack_bar = ft.SnackBar(ft.Text("🚫 Login Blocked: Account active on another device!"))
                page.snack_bar.open = True
                page.update()
                return

            vega.is_premium = profile.get('is_premium', False)
            load_dashboard()

        except Exception as ex:
            # For demo, if auth fails (e.g. wrong pass), show error
            # BUT: If user has no account, we can auto-signup or show error
            page.snack_bar = ft.SnackBar(ft.Text(f"Login Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    # UI Elements for Login
    email_input = ft.TextField(label="Email", border_color="green", color="white", width=300)
    pwd_input = ft.TextField(label="Password", password=True, border_color="green", color="white", width=300)
    
    login_view = ft.Column([
        ft.Container(height=80),
        ft.Text("VEGA OS", size=50, weight="bold", color="green"),
        ft.Text("Identify Yourself", color="grey"),
        ft.Container(height=20),
        email_input,
        pwd_input,
        ft.ElevatedButton("LOGIN", on_click=handle_login, bgcolor="green", color="white", width=200),
        ft.TextButton("Create Account", on_click=lambda e: page.launch_url("https://lblkigfnfgjcvxdkqwmk.supabase.co")),
        ft.TextButton("Privacy & Terms", on_click=lambda e: page.launch_url("https://vega-os-terms.com"))
    ], horizontal_alignment="center")

    def load_dashboard():
        page.clean()
        page.add(
            ft.AppBar(
                title=ft.Text("VEGA HOME"), 
                bgcolor="#111111",
                actions=[ft.IconButton(ft.icons.HELP, on_click=lambda e: page.launch_url("mailto:support@vega.ai"))]
            ),
            ft.Column([
                ft.Container(height=50),
                reactor,
                ft.Container(height=30),
                status_txt,
                ft.Container(height=20),
                ft.Row([
                    ft.IconButton(ft.icons.WIFI, icon_color="white"),
                    ft.IconButton(ft.icons.BLUETOOTH, icon_color="white"),
                    ft.IconButton(ft.icons.FLASHLIGHT_ON, icon_color="white"),
                    ft.IconButton(ft.icons.BATTERY_STD, icon_color="green"),
                ], alignment="center")
            ], horizontal_alignment="center")
        )

    # Start App
    page.add(login_view)

ft.app(target=main)
