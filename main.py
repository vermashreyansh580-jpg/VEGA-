import flet as ft

def main(page: ft.Page):
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Simple Neon UI check
    page.add(
        ft.Icon(ft.icons.CHECK_CIRCLE, size=100, color="green"),
        ft.Text("SYSTEM ONLINE", size=30, color="green", weight="bold"),
        ft.Text("Core UI Loaded Successfully", color="white")
    )

ft.app(target=main)
