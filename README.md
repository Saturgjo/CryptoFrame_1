## Popis projektu

Tento projekt obsahuje dva hlavní programy:

- `CryptoFrame_copy4.py`
- `CryptoFrame_copy3.py`

### Požadavky a instalace

Pro správný běh skriptů je nutné nainstalovat následující nástroje. Doporučuje se instalovat je na disk, který budete používat pro tento projekt.

Nejprve nainstalujte [Chocolatey](https://chocolatey.org/install), pokud jej ještě nemáte. Poté spusťte následující příkazy v příkazovém řádku s administrátorskými právy:

```bash
choco install ffmpeg
choco install steghide
```
Příklad kde jsem pracoval s projektem a kde se instalovali.

![image](https://github.com/user-attachments/assets/c7aa9e1d-9c6f-4fef-8b42-c2ec5e385c37)


### CryptoFrame_copy4.py

Tento program umožňuje přidávání metadat do audio záznamů pomocí steganografie. Pro správnou funkci je třeba upravit následující části v kódu:

1. **Cíl přidání metadat**:
   - Ve spodní části kódu upravte cestu k souboru, do kterého chcete přidat metadata.

2. **Heslo**:
   - Najděte řádek `password = ""` a nastavte silné heslo, aby nebylo možné data snadno ověřit třetími stranami. *(Toto nastavení platí pouze pro audio záznamy.)*

3. **Umístění souboru `message.txt`**:
   - Ve spodní části kódu můžete upravit cestu k souboru `message.txt` podle vašich potřeb.

4. **Nastavení metadat**:
   - Nastavte hodnoty metadat, jako jsou `user_name` a `user_id`.
  
5. **Cíl exportu metadat**:
   - Ve spodní části kódu můžete upravit cestu kam soubor bude putovat nebo je možno v konzoli zadat vlastní cestu při vytváření
   - "Buď ve chvíli kdy se konzile zeptá kam soubor pošlete napíšete vlastní nebo jen potvrdíte"

**Spuštění programu:**
```bash
python .\CryptoFrame_copy4.py
```

### CryptoFrame_copy3.py

Tento program slouží k ověřování videí a sledování jejich stažení. Pro správnou funkci je třeba upravit následující části v kódu:

1. **Výběr videa**:
   - Ve spodní části kódu určete, které video/audio chcete ověřit a zjistit, kdo jej stáhl.

2. **Zobrazení metadat**:
   - Metadata se zobrazí v konzoli.

3. **Export `message.txt`**:
   - Soubor `message.txt` z audio záznamu se exportuje do složky s kódem.
   - U video souboru se zobrazí metadata, ale může dojít k chybě („error“) týkající se nepřítomnosti souboru `message.txt`.

**Spuštění programu:**
```bash
python .\CryptoFrame_copy3.py
```

### Poznámky

- Ujistěte se, že máte nainstalované všechny potřebné závislosti pro běh skriptů.
- Doporučuje se používat bezpečné heslo pro ochranu dat.
- Při úpravě cest k souborům dbejte na správnou strukturu složek ve vašem projektu.

Pokud máte jakékoliv otázky nebo potřebujete pomoc, neváhejte v repozitáři nebo kontaktovat autora projektu.

## Příklad použití

1. **Přidání metadat do video/audio záznamu:**
   ```bash
   python .\CryptoFrame_copy4.py
   ```

2. **Ověření videa/audia a sledování stažení:**
   ```bash
   python .\CryptoFrame_copy3.py
   ```
