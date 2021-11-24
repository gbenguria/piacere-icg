def vmcatalog1 (vcpu, gib, sigla):
    vcpu = str(vcpu)
    gib = str(gib)
    if sigla == "mac" and vcpu=='12' and gib=='32':
        return "mac1.metal"
    elif sigla == "t2":
        if vcpu == '1':
            if gib == '0.5':
                return "t2.nano"
            elif gib == '1':
                return "t2.micro"
            elif gib == '2':
                return "t2.small"
        elif vcpu == '2':
            if gib == '4':
                return "t2.medium"
            elif gib == '8':
                return "t2.large"
        elif vcpu == '4' and gib == '16':
            return "t2.xlarge"
        elif vcpu == '8' and gib == '32':
            return "t2.2xlarge"
    elif sigla == "m6g" or sigla == "m6gd":
        if vcpu == '1' and gib == '4':
            return sigla+".medium"
        if vcpu == '2' and gib == '8':
            return sigla+".large"
        if vcpu == '4' and gib == '16':
            return sigla+".xlarge"
        if vcpu == '8' and gib == '32':
            return sigla+".2xlarge"
        if vcpu == '16' and gib == '64':
            return sigla+".4xlarge"
        if vcpu == '32' and gib == '128':
            return sigla+".8xlarge"
        if vcpu == '48' and gib == '192':
            return sigla+".12xlarge"
        if vcpu == '64' and gib == '256':
            return sigla+".16xlarge"
    elif "m5" in sigla or sigla == "m4":
        if vcpu == '2' and gib == '8':
            return sigla+".large"
        if vcpu == '4' and gib == '16':
            return sigla+".xlarge"
        if vcpu == '8' and gib == '32':
            return sigla+".2xlarge"
        if vcpu == '16' and gib == '64':
            return sigla+".4xlarge"
        if vcpu == '32' and gib == '128':
            return sigla+".8xlarge"
        if vcpu == '48' and gib == '192':
            return sigla+".12xlarge"
        if vcpu == '64' and gib == '256':
            return sigla+".16xlarge"
        if vcpu == '96' and gib == '384':
            return sigla+".24xlarge"
    elif sigla == "a1":
        if vcpu == '1' and gib == '2':
            return "a1.media"
        if vcpu == '2' and gib == '4':
            return "a1.large"
        if vcpu == '4' and gib == '8':
            return "a1.xlarge"
        if vcpu == '8' and gib == '16':
            return "a1.2xlarge"
        if vcpu == '16' and gib == '32':
            return "a1.4xlarge"
    elif vcpu=='2':
        if gib == '0.5':
            return sigla+".nano"
        elif gib == '1':
            return sigla+".micro"
        elif gib == '2':
            return sigla+".small"
        elif gib == '4':
            return sigla+".medium"
        elif gib == '8':
            return sigla+".large"
    elif vcpu == '4' and gib == '16':
        return sigla+".xlarge"
    elif vcpu == '8' and gib == '32':
        return sigla+".2xlarge"
    return "t3.micro"

def vmcatalog (vcpu, gib):
    vcpu = str(vcpu)
    gib = str(gib)
    if vcpu=='12' and gib=='32':
        return "mac1.metal"
    if vcpu == '1':
        if gib == '0.5':
            return "t2.nano"
        if gib == '1':
            return "t2.micro"
        if gib == '2':
            return "t2.small"
    if vcpu == '2':
        if gib == '4':
            return "t2.medium"
        if gib == '8':
            return "t2.large"
        if vcpu == '4' and gib == '16':
            return "t2.xlarge"
        if vcpu == '8' and gib == '32':
            return "t2.2xlarge"
    if vcpu == '1' and gib == '4':
        return "m6g.medium"
    if vcpu == '2' and gib == '8':
        return "m6g.large"
    if vcpu == '4' and gib == '16':
        return "m6g.xlarge"
    if vcpu == '8' and gib == '32':
        return "m6g.2xlarge"
    if vcpu == '16' and gib == '64':
        return "m6g.4xlarge"
    if vcpu == '32' and gib == '128':
        return "m6g.8xlarge"
    if vcpu == '48' and gib == '192':
        return "m6g.12xlarge"
    if vcpu == '64' and gib == '256':
        return "m6g.16xlarge"
    if vcpu == '2' and gib == '8':
        return "m4.large"
    if vcpu == '4' and gib == '16':
        return "m4.xlarge"
    if vcpu == '8' and gib == '32':
        return "m4.2xlarge"
    if vcpu == '16' and gib == '64':
        return "m4.4xlarge"
    if vcpu == '32' and gib == '128':
            return "m4.8xlarge"
    if vcpu == '48' and gib == '192':
        return "m4.12xlarge"
    if vcpu == '64' and gib == '256':
            return "m4.16xlarge"
    if vcpu == '96' and gib == '384':
        return "m4.24xlarge"
    if vcpu == '1' and gib == '2':
        return "a1.media"
    if vcpu == '2' and gib == '4':
        return "a1.large"
    if vcpu == '4' and gib == '8':
        return "a1.xlarge"
    if vcpu == '8' and gib == '16':
        return "a1.2xlarge"
    if vcpu == '16' and gib == '32':
        return "a1.4xlarge"
    if vcpu=='2':
        if gib == '0.5':
            return "t3.nano"
        if gib == '1':
            return "t3.micro"
        if gib == '2':
            return "t3.small"
        if gib == '4':
            return "t3.medium"
        if gib == '8':
            return "t3.large"
    if vcpu == '4' and gib == '16':
        return "t3.xlarge"
    if vcpu == '8' and gib == '32':
        return "t3.2xlarge"
    return "t2.micro"
