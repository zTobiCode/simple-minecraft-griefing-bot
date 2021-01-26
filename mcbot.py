# simple griefing bot by t.me/wejdene lol

import re
import uuid
import hashlib
import socket
import struct
import shodan
import random
import discord
import asyncio
import requests
import mcstatus
import datetime
import dns.resolver
import nmap

TOKEN = '' # put your bot's token here
PREFIX = '#'

SHODAN_API_KEY = '' # shodan.io API key

client = discord.Client()

async def get_server_informations(ip) -> discord.Embed():
    try:
        server = mcstatus.MinecraftServer.lookup(ip)
        status = server.status()

        fields = {
            'Host': '%s:%s (%s)' % (server.host, str(server.port), socket.gethostbyname(server.host)) if socket.gethostbyname(server.host) != server.host else '%s:%s' % (server.host, str(server.port)),
            'Version': '%s - %s' % (status.version.name, str(status.version.protocol)),
            'Players': '%s/%s' % (str(status.players.online), str(status.players.max)),
            'Motd': re.sub(r'\ +', ' ', re.sub(r'(&|§)[a-z0-9]{1}|\n||\\n', '', ''.join([x.split('\'')[0] for x in str(status.description).split('\'text\': \'')])).replace('{', ''))
        }
        
        embed = discord.Embed(title="Server Informations", description='Get Minecraft server\'s informations', color=0xffffff)

        for key, value in fields.items():
            embed.add_field(
                name='» %s' % key,
                value='`%s`' % value,
                inline=False
            )

        embed.set_thumbnail(url='https://eu.mc-api.net/v3/server/favicon/%s:%s' % (server.host, str(server.port)))
        return embed, True
    except:
        return error('can\'t lookup the server.'), False

def error(message):
    return discord.Embed(title='❌  **error**  ❌', description=message, colour=discord.Colour.red())

def warning(message):
    return discord.Embed(title='💥  **warning**  💥', description=message, colour=0xe7e33c)

def success(message):
    return discord.Embed(title='✅  **success**  ✅', description=message, colour=discord.Colour.green())

@client.event
async def on_ready():
    print('[+] bot is ready !')

@client.event
async def on_message(x):
    try:
        content = x.content
        author = x.author

        arguments = str(content).split()
        command = arguments[0]



        if command.startswith(PREFIX):
            print('[+] \'%s\' executed \'%s\' with args: \'%s\'' % (author, command, ' '.join(arguments[1:])))
        
            command = command[len(PREFIX):].lower()

            if command == 'help':
                embed = discord.Embed(title="Help Menu ", description="Here's the command list with descriptions.", color=0xffffff)
                embed.add_field(name=PREFIX + "help", value=":sparkles: `show this menu`", inline=False)
                embed.add_field(name=PREFIX + "server", value=":sparkles: `lookup a Minecraft server`", inline=False)
                embed.add_field(name=PREFIX + "player", value=":sparkles: `lookup a Minecraft player`", inline=False)
                embed.add_field(name=PREFIX + "subdomains", value=":sparkles: `get subdomains from a domain (bruteforce)`", inline=False)
                embed.add_field(name=PREFIX + "bungeesearch", value=":sparkles: `get random bungeecord servers`", inline=False)
                embed.add_field(name=PREFIX + "lookup", value=":sparkles: `lookup a minecraft version`", inline=False)
                embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/763921786898874398.gif?v=1')
                await x.channel.send(embed=embed)

            elif command == 'scan':
                try:
                    ip = arguments[1]
                    ports = arguments[2]
                except IndexError:
                    await x.channel.send(embed=error('Please provide an ip to scan and a port range'))
                    return
                chars = '/*-'
                for char in chars:
                    if char in ip:
                        await x.channel.send(embed=warning('you can only scan single hosts, not ip ranges'))
                        return

                chars = '<>^|;\'"!?[]()`'
                for char in chars:
                    if char in ip or char in ports:
                        await x.channel.send(embed=warning('no!'))
                        return                
                try:
                    scanner = nmap.PortScanner()
                    scanner.scan(
                        hosts=ip,
                        ports=ports,
                        arguments='-n -Pn --open --exclude-ports 21,22,53,80,81,111,3306,2022,8096 --privileged --max-hostgroup 1 -sS -r'
                    )

                    output = scanner.csv().splitlines()
                    for line in output:
                        try:
                            ip = line.split(';')[0]
                            port = line.split('tcp;')[1].split(';')[0]
                            e, s = await get_server_informations('%s:%s' % (ip, port))
                            if s == True:
                                await x.channel.send(embed=e)
                        except:
                            pass
                except:
                    pass
                await x.channel.send(embed=success('done.'))

            elif command == 'subdomains':
                subdomains_list = ["www",'scrub','spark',"uhc", "serieyt", "shop", "report", "apply", "youtube", "twitter", "st", "lost", "sg", "srvc1","srvc2","srvc3","srvc4", "torneo", "serv11", "serv0", "serv10", "serv9", "serv7", "serv6", "serv5", "serv4", "serv3", "serv2", "serv1", "serv", "mcp", "paysafe", "mu", "radio", "donate", "vps03", "vps02", "vps01", "xenon", "radio", "bans", "ns2", "ns1", "donar", "radio", "new", "appeals", "reports", "translations", "marketing", "staff", "bugs", "help", "render", "foro", "ts3", "git", "analytics", "coins", "votos", "docker-main", "main", "server3", "cdn", "creativo", "yt2", "yt", "factions", "solder", "test1", "test001", "testpene", "test", "panel", "apolo", "sv3", "sv2", "sv1", "backups", "zeus", "thor", "vps", "build", "web", "dev", "staff", "mc", "play", "sys", "node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8", "node9", "node10", "node11", "node12", "node13", "node14", "node15", "node16", "node17", "node18", "node19", "node20", "node001", "node002", "node01", "node02", "node003", "sys001", "sys002", "go", "admin", "eggwars", "bedwars", "lobby1", "hub", "builder", "developer", "test1", "forum", "bans", "baneos", "ts", "sys1", "sys2", "mods", "bungee", "bungeecord", "array", "spawn", "help", "client", "api", "smtp", "s1", "s2", "s3", "s4", "server1", "server2", "jugar", "login", "mysql", "phpmyadmin", "demo", "na", "eu","sa", "us", "es", "fr", "it", "ru", "support", "developing", "discord", "backup", "buy", "buycraft", "go", "dedicado1", "dedi", "dedi1", "dedi2", "dedi3", "minecraft", "prueba", "pruebas", "ping", "register", "cdn", "stats", "store", "serie", "buildteam", "info", "host", "jogar", "proxy", "vps", "ovh", "partner", "partners", "appeals", "appeal", "store-assets", "builds", "testing", "server", "pvp", "skywars", "survival", "skyblock", "lobby", "hg", "games", "sys001", "sys002", "node001", "node002", "games001", "games002", "game001", "game002", "game003", "sys001", "us72", "us1", "us2", "us3", "us4", "us5", "goliathdev", "staticassets", "rewards", "rpsrv", "ftp", "ssh", "web", "jobs", "render", "hcf", "grafana", "vote2", "file", "sentry", "enjin", "webserver", "xen", "mco", "monitor", "servidor2", "sadre", "gamehitodrh",'dev321','dev123']
                try:
                    domain = arguments[1]
                except IndexError:
                    await x.channel.send(embed=error('Please provide a domain to scan'))
                    return
                
                for subdomain in subdomains_list:
                    try:
                        ip = socket.gethostbyname('%s.%s' % (subdomain, domain))
                        ips = []
                        ips.append(ip)
                        r = dns.resolver.query(qname=ip, rdtype='A')
                        for rdata in r:
                            ip = rdata.to_text()
                            if not ip in str(ips):
                                ips.append(ip)
                        await x.channel.send('🚘 subdomain  found: `%s.%s` 👉 (`%s`)' % (subdomain, domain, ','.join(ips)))
                    except Exception as e:
                        pass
                await x.channel.send(embed=success('done.'))

            elif command == 'bungeesearch':
                urls = [
                    ('https://minecraft-mp.com/type/bungeecord/', (1, 40)),
                    ('https://minecraft-mp.com/type/waterfall/', (1, 5))
                ]

                url, _range = random.choice(urls)
                page = random.randint(_range[0], _range[1])

                url = '%s%s/' % (url, str(page))

                r = requests.get(url)
                ips = re.findall(r'</a>&nbsp;<strong>(.*?)</strong>', r.text)
                for ip in ips:
                    e, s = await get_server_informations(ip)
                    if s == True:
                        await x.channel.send(embed=e)
                await x.channel.send(embed=success('done.'))

            elif command == 'player':
                try:
                    target = arguments[1]
                except IndexError:
                    await x.channel.send(embed=error('Please provide a username to lookup'))
                    return
                try:
                    online_uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + target).json()['id']
                    online_uuid_dashed = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:21]}-{online_uuid[21:32]}'
                except (KeyError, ValueError, IndexError):
                    online_uuid_dashed = '-'
                    online_uuid = '-'
            
                offline_uuid_dashed = str(uuid.UUID(bytes=hashlib.md5(bytes('OfflinePlayer:' + target, 'utf-8')).digest()[:16], version=3))
                offline_uuid = offline_uuid_dashed.replace('-', '')
                nickname_history = {target: '-'}
                if len(online_uuid) > 1:
                    nickname_history = {}
                    json_data = requests.get(f'https://api.mojang.com/user/profiles/{online_uuid}/names').json()
                    for _x in json_data:
                        try:
                            try:
                                date = datetime.datetime.fromtimestamp(float(_x['changedToAt'])/1000).strftime("%Y/%m/%d @ %H:%M:%S")
                            except Exception as e:
                                date = '-'
                            nickname_history[_x['name']] = date
                        except:
                            pass
                embed = discord.Embed(title="Player Informations", description='Get Minecraft player\'s informations', color=0xffffff)
                
                embed.add_field(name='» Premium UUID', value='`%s`\n`%s`' % (online_uuid, online_uuid_dashed), inline=False)
                embed.add_field(name='» Offline UUID', value='`%s`\n`%s`' % (offline_uuid, offline_uuid_dashed), inline=False)
                embed.add_field(name='» Nicknames History', value='\n'.join(['`%s @ %s`' % (nick, date) for nick, data in nickname_history.items()]) if nickname_history != {target: '-'} else '`-`', inline=False)

                embed.set_thumbnail(url='https://visage.surgeplay.com/bust/512/%s' % online_uuid if online_uuid != '-' else 'https://visage.surgeplay.com/bust/512/8667ba71b85a4004af54457a9734eed7')

                await x.channel.send(embed=embed)

            elif command == 'lookup':
                if SHODAN_API_KEY == '':
                    await x.channel.send(embed=error('You must set-up a Shodan API key before using `lookup` command'))
                    return
                try:
                    query = ' '.join(arguments[1:])
                    if query == '':
                        await x.channel.send(embed=error('Please provide a query to search'))
                        return
                    cli = shodan.Shodan(SHODAN_API_KEY)
                    matches = cli.search(query=query)['matches']
                    for match in matches:
                        e, s = await get_server_informations('%s:%s' % (match['ip_str'], str(match['port'])))
                        if s == True:
                            await x.channel.send(embed=e)
                    await x.channel.send(embed=success('done.'))
                except:
                    await x.channel.send(embed=success('done.'))

            elif command == 'server':
                try:
                    ip = arguments[1]
                except IndexError:
                    await x.channel.send(embed=error('Please provide an IP to lookup'))
                    return
                e, _ = await get_server_informations(ip)
                await x.channel.send(embed=e)

    except IndexError:
        pass


client.run(
    TOKEN
)
