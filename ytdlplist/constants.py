import colorama

colorama.init()


RED, GREEN, YELLOW, MAGENTA, CYAN, DARK, WHITE, RESET = [
    colorama.Fore.LIGHTRED_EX,
    colorama.Fore.GREEN,
    colorama.Fore.YELLOW,
    colorama.Fore.MAGENTA,
    colorama.Fore.LIGHTCYAN_EX,
    colorama.Fore.LIGHTBLACK_EX,
    colorama.Fore.LIGHTWHITE_EX,
    colorama.Style.RESET_ALL,
]

BANNER = b"//6IJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCUKAIgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJQoAiCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYglkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMlkyWTJZMliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYgliCWIJYglCgCIJYgliCWIJSAAIAAgACAAIAAgACAAiCWIJZMlIAAgACAAIAAgACAAIAAgAJMlkyWTJSAAIAAgACAAIAAgAJMlkyUgACAAIAAgACAAIAAgACAAkyWTJSAAIAAgACAAIAAgAJMlkyWTJSAAIACTJZMlkyUgACAAiCWIJSAAIAAgACAAIAAgAIgliCWIJYgliCUKAIgliCWIJYglIAAgAIgliCWIJYglIAAgAJMlkyWTJZMlkyWTJSAAIACTJZMlkyWTJSAAIACTJZMlkyWTJZMlkyWTJZMlkyWTJSAAIACTJZMlkyWTJSAAIACTJZMlkyWTJSAAIACTJSAAIAAgAJMlkyUgACAAIACTJSAAIACIJYgliCWIJSAAIACIJYgliCWIJQoAiCWIJYgliCUgACAAiCWIJZMlkyUgACAAkyWTJZMlkyWTJZMlIAAgAJMlkyWTJZMlkyUgACAAIAAgACAAIACTJZMlkyWTJZMlIAAgAJMlkyWTJZMlIAAgAJMlkyWTJZMlIAAgAJMlIAAgACAAIAAgACAAIAAgAJMlIAAgACAAIAAgACAAIACIJYgliCWIJYglCgCIJYgliCWIJSAAIACTJZMlkyWTJSAAIACTJSAAIACTJZMlkyUgACAAkyWTJZIlkiWSJZIlkiWSJZIlkiUgACAAkiWSJZIlkiUgACAAkiWSJZIlkiUgACAAkiWSJZIlkiUgACAAkyUgACAAkyUgACAAkyUgACAAkyUgACAAkyWTJZMlkyWIJYgliCWIJYgliCUKAIgliCWIJYglIAAgACAAIAAgACAAIACTJZMlkyUgACAAIAAgACAAkiWSJZIlkiWSJZIlIAAgACAAIAAgACAAkiWSJZIlkiWSJSAAIACSJZIlkiWSJZIlIAAgACAAIAAgACAAkiWSJSAAIACSJZIlkiWTJSAAIACTJSAAIACTJZMlkyWTJZMlkyWIJYgliCWIJQoAiCWIJZMlkyWTJZMlkyWTJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWTJZMlkyWTJZMlkyWIJYglCgCIJZMlkyWTJZMlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZIlkiWSJZMlkyWTJZMliCUKAJMlkyWTJZIlkiWSJZIlkiWSJZIlkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElIACpAEQASgAgAFMAdABvAG0AcAAgADIAMAAyADQAIACRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWSJZIlkiWSJZIlkiWSJZMlkyWTJQoAkyWTJZIlkiWSJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSUgACIATgBvACAAUgBpAGcAaAB0AHMAIABSAGUAcwBlAHIAdgBlAGQAIgAgAJElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWSJZIlkiWTJZMlCgCTJZIlkiWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWSJZIlkyUKAJIlkiWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkSWRJZElkiWSJQoA"