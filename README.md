# python.ssh-key-manager
 Pequeño proyecto para la gestión de las llaves SSH autorizadas dentro de una máquina, permite añadir o eliminar las llaves de una forma sencilla y centralizada.

 Proyecto creado en un principio para la red de IRC "GlobalChat IRC Network" y las máquinas que la asociación mantenía.

# Comandos disponibles
 * --restore, Restaura las rsa keys de /etc/ssh/keys-enabled/
 * --install [archivo], Activa una rsa key
 * --install-all, Activa las rsa keys de /etc/ssh/keys-available/
 * --remove [archivo], Elimina una rsa key activa
 * --remove-all, Elimina las rsa keys de /etc/ssh/keys-enabled/
