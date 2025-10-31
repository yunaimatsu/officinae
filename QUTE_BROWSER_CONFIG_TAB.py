def tab(c, config):
    # bg-color of the tab bar 
    config.set('colors.tabs.bar.bg', '#1e1e1e')
    config.set('colors.webpage.darkmode.enabled', True)

    ## Non-selected
    config.set('colors.tabs.even.bg', '#222222')
    config.set('colors.tabs.odd.bg', '#444444')
    config.set('colors.tabs.even.fg', '#aaaaaa')
    config.set('colors.tabs.odd.fg', '#aaaaaa')

    ## Selected
    config.set('colors.tabs.selected.even.bg', '#aaaaaa')
    config.set('colors.tabs.selected.odd.bg', '#aaaaaa')
    config.set('colors.tabs.selected.even.fg', '#111111')
    config.set('colors.tabs.selected.odd.fg', '#111111')

    ## Tab box 
    c.tabs.padding = {'top': 6, 'bottom': 6, 'left': 4, 'right': 4 }
    c.tabs.favicons.show = 'never'
