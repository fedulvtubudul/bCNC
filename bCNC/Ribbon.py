#
# Author: vvlachoudis@gmail.com
# Date: 18-Jun-2015

from tkinter import (
    TclError,
    FALSE,
    YES,
    TRUE,
    X,
    Y,
    BOTH,
    LEFT,
    TOP,
    RIGHT,
    BOTTOM,
    RAISED,
    FLAT,
    GROOVE,
    NORMAL,
    DISABLED,
    StringVar,
    Button,
    Checkbutton,
    Frame,
    Label,
    Menu,
    Radiobutton,
)

import Utils
import tkExtra

__author__ = "Vasilis Vlachoudis"
__email__ = "vvlachoudis@gmail.com"

_TABFONT = ("Sans", "-14", "bold")
_FONT = ("Sans", "-11")

_BACKGROUND_DISABLE = "#A6A2A0"
_BACKGROUND_TAB_SELECT = "#E5E2E0"
_BACKGROUND = "#E5E2E0"
_BACKGROUND_GROUP = "#B6B2B0"

_BACKGROUND_GROUP2 = "#B0C0C0"
_BACKGROUND_GROUP3 = "#A0C0A0"
_BACKGROUND_GROUP4 = "#B0C0A0"

_FOREGROUND_GROUP = "White"
_ACTIVE_COLOR = "LightYellow"
_LABEL_SELECT_COLOR = "#C0FFC0"

# Ribbon show state
RIBBON_HIDDEN = 0  # Hidden
RIBBON_SHOWN = 1  # Displayed
RIBBON_TEMP = -1  # Show temporarily


# =============================================================================
# Frame Group with a button at bottom
# =============================================================================
class LabelGroup(Frame):
    def __init__(self, master, name, command=None, **kw):
        Frame.__init__(self, master, **kw)
        self.name = name
        self.config(
            background=_BACKGROUND, borderwidth=0, highlightthickness=0, pady=0
        )

        # right frame as a separator
        f = Frame(self, borderwidth=2,
                  relief=GROOVE, background=_BACKGROUND_DISABLE)
        f.pack(side=RIGHT, fill=Y, padx=0, pady=0)

        # frame to insert the buttons
        self.frame = Frame(
            self,
            background=_BACKGROUND,
            padx=0,
            pady=0,
        )
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH, padx=0, pady=0)

        if command:
            self.label = LabelButton(self, self, f"<<{name}>>", text=name)
            self.label.config(
                command=command,
                image=Utils.icons["triangle_down"],
                foreground=_FOREGROUND_GROUP,
                background=_BACKGROUND_GROUP,
                highlightthickness=0,
                borderwidth=0,
                pady=0,
                compound=RIGHT,
            )
        else:
            self.label = Label(
                self,
                text=_(name),
                font=_FONT,
                foreground=_FOREGROUND_GROUP,
                background=_BACKGROUND_GROUP,
                padx=2,
                pady=0,
            )  # Button takes 1px for border width
        self.label.pack(side=BOTTOM, fill=X, pady=0)

    # -----------------------------------------------------------------------
    def grid2rows(self):
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

    # -----------------------------------------------------------------------
    def grid3rows(self):
        self.grid2rows()
        self.frame.grid_rowconfigure(2, weight=1)


# =============================================================================
class _KeyboardFocus:
    # -----------------------------------------------------------------------
    def _bind(self):
        self.bind("<Return>", self._invoke)
        self.bind("<FocusIn>", self._focusIn)
        self.bind("<FocusOut>", self._focusOut)

    # -----------------------------------------------------------------------
    def _focusIn(self, event):
        self.__backgroundColor = self.cget("background")
        self.config(background=_ACTIVE_COLOR)

    # -----------------------------------------------------------------------
    def _focusOut(self, event):
        self.config(background=self.__backgroundColor)

    # -----------------------------------------------------------------------
    def _invoke(self, event):
        self.invoke()


# =============================================================================
# Flat button drawn as a Label, some systems ignore the button background
# =============================================================================
class _FlatButton(Label):
    def __init__(self, master, command=None, **kw):
        self._command = command
        kw.setdefault("takefocus", True)
        Label.__init__(self, master, **kw)
        self.bindtags((str(self), "RibbonFlatButton") + self.bindtags()[1:])
        self.bind_class("RibbonFlatButton", "<ButtonRelease-1>", _FlatButton._click)
        self.bind("<space>", lambda e: self.invoke())

    # -----------------------------------------------------------------------
    @staticmethod
    def _click(event):
        button = event.widget
        if not isinstance(button, _FlatButton):
            return
        if 0 <= event.x < button.winfo_width() and 0 <= event.y < button.winfo_height():
            button.invoke()

    # -----------------------------------------------------------------------
    def configure(self, cnf=None, **kw):
        if "command" in kw:
            self._command = kw.pop("command")
            if cnf is None and not kw:
                return None
        return Label.configure(self, cnf, **kw)

    config = configure

    # -----------------------------------------------------------------------
    def __setitem__(self, key, value):
        if key == "command":
            self._command = value
        else:
            Label.__setitem__(self, key, value)

    # -----------------------------------------------------------------------
    def cget(self, key):
        if key == "command":
            return self._command
        return Label.cget(self, key)

    __getitem__ = cget

    # -----------------------------------------------------------------------
    def invoke(self):
        if str(self.cget("state")) == DISABLED:
            return None
        if self._command is not None:
            return self._command()
        return None


# =============================================================================
# Button with Label that generates a Virtual Event or calls a command
# =============================================================================
class LabelButton(_FlatButton, _KeyboardFocus):
    def __init__(self, master, recipient=None, event=None, **kw):
        _FlatButton.__init__(self, master, **kw)
        self.config(
            relief=FLAT,
            activebackground=_ACTIVE_COLOR,
            font=_FONT,
            borderwidth=1,
            highlightthickness=0,
            padx=2,
            pady=0,
        )
        _KeyboardFocus._bind(self)
        if recipient is not None:
            self.config(command=self.sendEvent)
            self._recipient = recipient
            self._event = event
        else:
            self._recipient = None
            self._event = None

    # -----------------------------------------------------------------------
    def sendEvent(self):
        self._recipient.event_generate(self._event)


# =============================================================================
class LabelCheckbutton(Checkbutton, _KeyboardFocus):
    def __init__(self, master, **kw):
        Checkbutton.__init__(self, master, **kw)
        self.config(
            selectcolor=_LABEL_SELECT_COLOR,
            activebackground=_ACTIVE_COLOR,
            background=_BACKGROUND,
            indicatoron=FALSE,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            font=_FONT,
        )
        _KeyboardFocus._bind(self)


# =============================================================================
class LabelRadiobutton(_FlatButton, _KeyboardFocus):
    def __init__(self, master, variable=None, value=None, **kw):
        self._variable = variable
        self._value = value
        self._focus = False
        _FlatButton.__init__(self, master, **kw)
        self.config(
            activebackground=_ACTIVE_COLOR,
            background=_BACKGROUND,
            borderwidth=0,
            highlightthickness=0,
            pady=0,
            font=_FONT,
        )
        _KeyboardFocus._bind(self)
        if self._variable is not None:
            self._variable.trace_add("write", self._changed)
        self.refresh()

    # -----------------------------------------------------------------------
    def configure(self, cnf=None, **kw):
        if "variable" in kw:
            self._variable = kw.pop("variable")
        if "value" in kw:
            self._value = kw.pop("value")
        return _FlatButton.configure(self, cnf, **kw)

    config = configure

    # -----------------------------------------------------------------------
    def invoke(self):
        if str(self.cget("state")) == DISABLED:
            return None
        if self._variable is not None:
            self._variable.set(self._value)
        return _FlatButton.invoke(self)

    # -----------------------------------------------------------------------
    def _changed(self, *args):
        try:
            self.refresh()
        except TclError:
            pass

    # -----------------------------------------------------------------------
    def refresh(self):
        if self._focus:
            color = _ACTIVE_COLOR
        elif self._variable is not None and self._variable.get() == self._value:
            color = _LABEL_SELECT_COLOR
        else:
            color = _BACKGROUND
        Label.configure(self, background=color)

    # -----------------------------------------------------------------------
    def _focusIn(self, event):
        self._focus = True
        self.refresh()

    # -----------------------------------------------------------------------
    def _focusOut(self, event):
        self._focus = False
        self.refresh()


# =============================================================================
class LabelCombobox(tkExtra.Combobox, _KeyboardFocus):
    def __init__(self, master, **kw):
        tkExtra.Combobox.__init__(self, master, **kw)
        self.config(background=_BACKGROUND, font=_FONT)
        Frame.config(self, background=_BACKGROUND, padx=0, pady=0)
        _KeyboardFocus._bind(self)

    # -----------------------------------------------------------------------
    def _focusOut(self, event):
        self.config(background=_BACKGROUND)  # self.__backgroundColor)
        Frame.config(self, background=_BACKGROUND)  # self.__backgroundColor)


# =============================================================================
# Button with Label that popup a menu
# =============================================================================
class MenuButton(_FlatButton, _KeyboardFocus):
    def __init__(self, master, menulist, **kw):
        _FlatButton.__init__(self, master, **kw)
        self.config(
            relief=FLAT,
            activebackground=_ACTIVE_COLOR,
            font=_FONT,
            borderwidth=0,
            highlightthickness=0,
            padx=2,
            pady=0,
            command=self.showMenu,
        )

        _KeyboardFocus._bind(self)
        self.bind("<Return>", self.showMenu)
        if menulist is not None:
            self._menu = MenuButton.createMenuFromList(self, menulist)
        else:
            self._menu = None

    # -----------------------------------------------------------------------
    def showMenu(self, event=None):
        if self._menu is not None:
            self._showMenu(self._menu)
        else:
            self._showMenu(self.createMenu())

    # -----------------------------------------------------------------------
    def _showMenu(self, menu):
        if menu is not None:
            menu.tk_popup(self.winfo_rootx(),
                          self.winfo_rooty() + self.winfo_height())

    # -----------------------------------------------------------------------
    def createMenu(self):
        return None

    # -----------------------------------------------------------------------
    @staticmethod
    def createMenuFromList(master, menulist):
        mainmenu = menu = Menu(master,
                               tearoff=0, activebackground=_ACTIVE_COLOR)
        for item in menulist:
            if item is None:
                menu.add_separator()
            elif isinstance(item, str):
                menu = Menu(mainmenu)
                mainmenu.add_cascade(label=item, menu=menu)
            else:
                name, icon, cmd = item
                if icon is None:
                    icon = "empty"
                menu.add_command(
                    label=name, image=Utils.icons[icon], compound=LEFT, command=cmd
                )
        return menu


# =============================================================================
# A label group with a drop down menu
# =============================================================================
class MenuGroup(LabelGroup):
    def __init__(self, master, name, menulist=None, **kw):
        LabelGroup.__init__(self, master, name, command=self._showMenu, **kw)
        self._menulist = menulist

    # -----------------------------------------------------------------------
    def createMenu(self):
        if self._menulist is not None:
            return MenuButton.createMenuFromList(self, self._menulist)
        else:
            return None

    # -----------------------------------------------------------------------
    def _showMenu(self):
        menu = self.createMenu()
        if menu is not None:
            menu.tk_popup(self.winfo_rootx(),
                          self.winfo_rooty() + self.winfo_height())


# =============================================================================
# Page Tab buttons
# =============================================================================
class TabButton(Label):
    def __init__(self, master, variable, value, command=None, **kw):
        Label.__init__(self, master, **kw)
        self._variable = variable
        self._value = value
        self._command = command
        self._focus = False
        self._hover = False
        self.config(
            relief=FLAT,
            font=_TABFONT,
            borderwidth=0,
            highlightthickness=0,
            padx=5,
            pady=0,
            takefocus=True,
        )
        self.bindtags((str(self), "RibbonTabButton") + self.bindtags()[1:])
        self.bind_class("RibbonTabButton", "<ButtonRelease-1>", TabButton._click)
        self.bind("<FocusIn>", self._focusIn)
        self.bind("<FocusOut>", self._focusOut)
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self._variable.trace_add("write", self.refresh)
        self.refresh()

    # -----------------------------------------------------------------------
    @staticmethod
    def _click(event):
        tab = event.widget
        if not isinstance(tab, TabButton):
            return
        if 0 <= event.x < tab.winfo_width() and 0 <= event.y < tab.winfo_height():
            tab.invoke()

    # -----------------------------------------------------------------------
    def invoke(self):
        self._variable.set(self._value)
        if self._command is not None:
            self._command()

    # -----------------------------------------------------------------------
    def refresh(self, *args):
        if self._variable.get() == self._value:
            color = _ACTIVE_COLOR if self._focus else _BACKGROUND_TAB_SELECT
        elif self._hover:
            color = _ACTIVE_COLOR
        else:
            color = _BACKGROUND_DISABLE
        self.config(background=color)

    # -----------------------------------------------------------------------
    def _enter(self, event=None):
        self._hover = True
        self.refresh()

    # -----------------------------------------------------------------------
    def _leave(self, event=None):
        self._hover = False
        self.refresh()

    # -----------------------------------------------------------------------
    # Bind events on TabFrame
    # ----------------------------------------------------------------------
    def bindClicks(self, tabframe):
        self.bind("<Double-1>", tabframe.double)
        self.bind("<Button-1>", tabframe.dragStart)
        self.bind("<B1-Motion>", tabframe.drag)
        self.bind("<ButtonRelease-1>", tabframe.dragStop)
        self.bind("<Control-ButtonRelease-1>", tabframe.pinActive)

        self.bind("<Left>", tabframe._tabLeft)
        self.bind("<Right>", tabframe._tabRight)
        self.bind("<Down>", tabframe._tabDown)

    # ----------------------------------------------------------------------
    def _focusIn(self, evenl=None):
        self._focus = True
        self.refresh()

    # ----------------------------------------------------------------------
    def _focusOut(self, evenl=None):
        self._focus = False
        self.refresh()


# =============================================================================
# Page
# =============================================================================
class Page:  # <--- should be possible to be a toplevel as well
    _motionClasses = (
        LabelButton,
        LabelRadiobutton,
        LabelCheckbutton,
        LabelCombobox,
        MenuButton,
    )
    _name_ = None
    _icon_ = None
    _doc_ = "Tooltip"

    # -----------------------------------------------------------------------
    def __init__(self, master, **kw):
        self.master = master
        self.name = self._name_
        self._icon = Utils.icons[self._icon_]
        self._tab = None  # Tab button
        self.ribbons = []
        self.frames = []
        self.init()
        self.create()

    # -----------------------------------------------------------------------
    # Override initialization
    # -----------------------------------------------------------------------
    def init(self):
        pass

    # -----------------------------------------------------------------------
    # The tab page can change master if undocked
    # -----------------------------------------------------------------------
    # FIXME XXX SHOULD BE REMOVED
    # -----------------------------------------------------------------------
    def create(self):
        self.createPage()

    # -----------------------------------------------------------------------
    # FIXME XXX SHOULD BE REMOVED
    # -----------------------------------------------------------------------
    def createPage(self):
        self.page = Frame(self.master._pageFrame)
        return self.page

    # -----------------------------------------------------------------------
    # Called when a page is activated
    # -----------------------------------------------------------------------
    def activate(self):
        pass

    # -----------------------------------------------------------------------
    def refresh(self):
        pass

    # ----------------------------------------------------------------------
    def canUndo(self):
        return True

    # ----------------------------------------------------------------------
    def canRedo(self):
        return True

    # ----------------------------------------------------------------------
    def resetUndo(self):
        pass

    # ----------------------------------------------------------------------
    def undo(self, event=None):
        pass

    # ----------------------------------------------------------------------
    def redo(self, event=None):
        pass

    # ----------------------------------------------------------------------
    def refreshUndoButton(self):
        # Check if frame provides undo/redo
        if self.master is None:
            return
        if self.page is None:
            return

        if self.canUndo():
            state = NORMAL
        else:
            state = DISABLED
        self.master.tool["undo"].config(state=state)
        self.master.tool["undolist"].config(state=state)

        if self.canRedo():
            state = NORMAL
        else:
            state = DISABLED
        self.master.tool["redo"].config(state=state)

    # -----------------------------------------------------------------------
    def keyboardFocus(self):
        self._tab.focus_set()

    # -----------------------------------------------------------------------
    # Return the closest widget along a direction
    # -----------------------------------------------------------------------
    @staticmethod
    def __compareDown(x, y, xw, yw):
        return yw > y + 1

    @staticmethod
    def __compareUp(x, y, xw, yw):
        return yw < y - 1

    @staticmethod
    def __compareRight(x, y, xw, yw):
        return xw > x + 1

    @staticmethod
    def __compareLeft(x, y, xw, yw):
        return xw < x - 1

    # -----------------------------------------------------------------------
    @staticmethod
    def __closest(widget, compare, x, y):
        closest = None
        dc2 = 10000000
        if widget is None:
            return closest, dc2
        for child in widget.winfo_children():
            for class_ in Page._motionClasses:
                if isinstance(child, class_):
                    if child["state"] == DISABLED:
                        continue
                    xw = child.winfo_rootx()
                    yw = child.winfo_rooty()
                    if compare(x, y, xw, yw):
                        d2 = (xw - x) ** 2 + (yw - y) ** 2
                        if d2 < dc2:
                            closest = child
                            dc2 = d2
                    break
            else:
                c, d2 = Page.__closest(child, compare, x, y)
                if d2 < dc2:
                    closest = c
                    dc2 = d2
        return closest, dc2

    # -----------------------------------------------------------------------
    # Select/Focus the closest element
    # -----------------------------------------------------------------------
    def _ribbonUp(self, event=None):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()
        closest, d2 = Page.__closest(self.ribbon, Page.__compareUp, x, y)
        if closest is not None:
            closest.focus_set()

    # -----------------------------------------------------------------------
    def _ribbonDown(self, event=None):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()
        closest, d2 = Page.__closest(self.ribbon, Page.__compareDown, x, y)
        if closest is not None:
            closest.focus_set()

    # -----------------------------------------------------------------------
    def _ribbonLeft(self, event=None):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()
        closest, d2 = Page.__closest(self.ribbon, Page.__compareLeft, x, y)
        if closest is not None:
            closest.focus_set()

    # -----------------------------------------------------------------------
    def _ribbonRight(self, event=None):
        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty()
        closest, d2 = Page.__closest(self.ribbon, Page.__compareRight, x, y)
        if closest is not None:
            closest.focus_set()


# =============================================================================
# TabRibbonFrame
# =============================================================================
class TabRibbonFrame(Frame):
    def __init__(self, master, **kw):
        Frame.__init__(self, master, kw)
        self.config(background=_BACKGROUND_DISABLE)

        self.oldActive = None
        self.activePage = StringVar(self)
        self.tool = {}
        self.pages = {}

        # === Top frame with buttons ===
        frame = Frame(self, background=_BACKGROUND_DISABLE)
        frame.pack(side=TOP, fill=X)

        # --- Basic buttons ---
        b = LabelButton(
            frame,
            self,
            "<<New>>",
            image=Utils.icons["new"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("New file"))
        b.pack(side=LEFT)

        b = LabelButton(
            frame,
            self,
            "<<Open>>",
            image=Utils.icons["load"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("Open file [Ctrl-O]"))
        b.pack(side=LEFT)

        b = LabelButton(
            frame,
            self,
            "<<Save>>",
            image=Utils.icons["save"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("Save all [Ctrl-S]"))
        b.pack(side=LEFT)

        b = LabelButton(
            frame,
            self,
            "<<Undo>>",
            image=Utils.icons["undo"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("Undo [Ctrl-Z]"))
        b.pack(side=LEFT)
        self.tool["undo"] = b

        b = LabelButton(
            frame,
            image=Utils.icons["triangle_down"],
            command=self.undolist,
            background=_BACKGROUND_DISABLE,
        )
        b.pack(side=LEFT)
        self.tool["undolist"] = b

        b = LabelButton(
            frame,
            self,
            "<<Redo>>",
            image=Utils.icons["redo"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("Redo [Ctrl-Y]"))
        b.pack(side=LEFT)
        self.tool["redo"] = b

        Label(frame, image=Utils.icons["sep"],
              background=_BACKGROUND_DISABLE).pack(
            side=LEFT, padx=3
        )

        # --- Help ---
        b = LabelButton(
            frame,
            self,
            "<<Help>>",
            image=Utils.icons["info"],
            background=_BACKGROUND_DISABLE,
        )
        tkExtra.Balloon.set(b, _("Help [F1]"))
        b.pack(side=RIGHT, padx=2)

        Label(frame, image=Utils.icons["sep"],
              background=_BACKGROUND_DISABLE).pack(
            side=RIGHT, padx=3
        )

        # --- TabBar ---
        self._tabFrame = Frame(frame, background=_BACKGROUND_DISABLE)
        self._tabFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        # ==== Ribbon Frame ====
        self._ribbonFrame = Frame(self, background=_BACKGROUND,
                                  pady=0, relief=RAISED)
        self._ribbonFrame.pack(fill=BOTH, expand=YES, padx=0, pady=0)

        self.setPageFrame(None)

    # -----------------------------------------------------------------------
    def setPageFrame(self, frame):
        self._pageFrame = frame

    # -----------------------------------------------------------------------
    def undolist(self, event=None):
        self.event_generate("<<UndoList>>")

    # -----------------------------------------------------------------------
    def getActivePage(self):
        return self.pages[self.activePage.get()]

    # -----------------------------------------------------------------------
    # Add page to the tabs
    # -----------------------------------------------------------------------
    def addPage(self, page, side=LEFT):
        self.pages[page.name] = page
        page._tab = TabButton(
            self._tabFrame,
            image=page._icon,
            text=_(page.name),
            compound=LEFT,
            value=page.name,
            variable=self.activePage,
            command=self.changePage,
        )
        tkExtra.Balloon.set(page._tab, page.__doc__)

        page._tab.pack(side=side, fill=Y, padx=5)

    # ----------------------------------------------------------------------
    # Unpack the old page
    # ----------------------------------------------------------------------
    def _forgetPage(self):
        if self.oldActive:
            for frame, args in self.oldActive.ribbons:
                frame.pack_forget()
            for frame, args in self.oldActive.frames:
                frame.pack_forget()
            self.oldActive = None

    # ----------------------------------------------------------------------
    # Change ribbon and page
    # ----------------------------------------------------------------------
    def changePage(self, page=None):
        if page is not None:
            if not isinstance(page, Page):
                try:
                    page = self.pages[page]
                except KeyError:
                    return
            self.activePage.set(page.name)
        else:
            try:
                page = self.pages[self.activePage.get()]
            except KeyError:
                return

        if page is self.oldActive:
            return

        self._forgetPage()

        for frame, args in page.ribbons:
            frame.pack(in_=self._ribbonFrame, **args)

        for frame, args in page.frames:
            frame.pack(in_=self._pageFrame, **args)

        self.oldActive = page
        page.activate()
        self.event_generate("<<ChangePage>>", data=page.name)
