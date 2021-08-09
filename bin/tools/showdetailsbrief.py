def showdetailsbrief(control):
    import yaml
    from platform import platform

    system = platform().lower()
    yaml_contet = yaml.safe_load(control['content'])['atomic_tests']
    dt_brief = [f'[{c + 1}] {yaml_contet[c]["name"]}' for c in range(0, len(yaml_contet)) if
        system.split('-')[0] in yaml_contet[c]['supported_platforms']]
    return dt_brief