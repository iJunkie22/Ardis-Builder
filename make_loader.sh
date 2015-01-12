#!/bin/bash

make_if_needed () {
    while read testdir;do if [ ! -d "$testdir" ];then mkdir "$testdir";fi;done
}
maintest_dir="$PWD"
user_local_bin="$HOME/.local/bin"
user_local_share="$HOME/.local/share"
user_local_share_apps="$HOME/.local/share/applications"
q_s='"'
d_s='$HOME'
make_if_needed "$user_local_bin"
make_if_needed "$user_local_share"
make_if_needed "$user_local_share_apps"
AB_bash_loader="$user_local_bin/ArdisBuilder"
AB_desktop_entry="$HOME/.local/share/applications/ArdisBuilder.desktop"
echo "#!/bin/bash
cd $q_s$maintest_dir$q_s
./main.py
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
Icon=$maintest_dir/icons/ardis-builder.png
MimeType=
Name[en_US]=Ardis Builder
Name=Ardis Builder
Path=
StartupNotify=true
Terminal=false
TerminalOptions=
Type=Application
Version=1.0
" > "$AB_desktop_entry"
chmod +x "$AB_desktop_entry"

exit