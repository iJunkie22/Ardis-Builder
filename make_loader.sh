#!/bin/bash
maintest_dir="$PWD"
user_local_bin="$HOME/.local/bin"
q_s='"'
d_s='$HOME'
if [ ! -d "$user_local_bin" ]
    then
    mkdir "$user_local_bin"
fi
AB_bash_loader="$user_local_bin/ArdisBuilder"
AB_desktop_entry="$HOME/.local/share/applications/ArdisBuilder.desktop"
echo "#!/bin/bash
cd $q_s$maintest_dir$q_s
./maintest.py
exit
" > "$AB_bash_loader"
chmod +x "$AB_bash_loader"

echo "[Desktop Entry]
Categories=Settings;
Comment[en_US]=
Comment=
Exec=$d_s/.local/bin/ArdisBuilder
GenericName[en_US]=Ardis Icon Theme Customization Wizard
GenericName=Ardis Icon Theme Customization Wizard
Icon=preferences-desktop-icons
MimeType=
Name[en_US]=Ardis Builder
Name=Ardis Builder
Path=
StartupNotify=true
Terminal=true
TerminalOptions=
Type=Application
Version=1.0
X-DBUS-ServiceName=
X-DBUS-StartupType=unique
X-KDE-SubstituteUID=false
X-KDE-Username=
" > "$AB_desktop_entry"
chmod +x "$AB_desktop_entry"

exit