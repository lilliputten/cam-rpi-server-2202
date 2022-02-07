<!--
 @changed 2022.02.07, 22:41
-->

# Cam flask photo receiver server & raspberry camera client


## Build info (auto-generated)

- Version: 0.0.2
- Last changes timestamp: 2022.02.08, 00:51
- Last changes timetag: 220208-0051


## API

Basic api structure:

TODO: Describe api (for specific server version)


## Server urls

Remote server: `http://cam-rpi-server.lilliputten.ru/`


## Server

Images server runs on python/flask platform.

TODO: Describe basic server functionality.

TODO: Preserve capability to implement public server (with same or like functinal?)


## Python venv maintenance

Server command for creating venv:

```
virtualenv -p python3 ~/.venv-py3-flask
source ~/.venv-py3-flask/bin/activate
pip install -r requirements.txt
```

Local script for venv creating and initialization:

```
sh utils/util-venv-init.sh
```

## Python dependencies

```
pip install PKGNAME
pip freeze > requirements-frozen.txt
pip install -r requirements.txt
```

## Camera interface

Camera shots are taken using the `raspistill` program using commands like:

```shell
# Default:
raspistill -o image.jpg
# Half:
raspistill -w 1296 -h 972 -o image-half.jpg
# Quarter:
raspistill -w 648 -h 486 -o image-quarter.jpg
```

For commandline reference use `raspistill --help`.

- [Camera configuration - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/configuration/camera.md)


## Raspberry camera client

Use `client-make-and-upload-image.sh` script to make & upload image to server.

Use crontab to automate image capture.

### Sample crontab lines:

- Every minute: `* * * * * /home/pi/projects/cam-rpi-server/client-make-and-upload-image.sh`
- Every 15th minute: `*/15 * * * * /home/pi/projects/cam-rpi-server/client-make-and-upload-image.sh`

## Real crontab entry example:

```shell
# Test entry...
30 */1 * * * date >> ~/test_crontab
*/5 * * * * date >> ~/test_crontab

# Make & upload shots every 5 minutes (with forced logging)...
*/5 * * * * sh /home/pi/projects/cam-rpi-server/client-make-and-upload-image.sh >> /home/pi/projects/cam-rpi-server/cron-log.txt 2>&1

# Make & upload shots every 20 minutes...
*/20 * * * * sh /home/pi/projects/cam-rpi-server/client-make-and-upload-image.sh

# Reboot every 3 hours (00:55, 03:55, etc...)
55 */3 * * * sudo reboot -f

# Start server on boot
@reboot sh /home/pi/projects/cam-rpi-server/utils/rpi-start-server.sh
```

### Crontab commands:

Edit crontab:
```shell
crontab -e
```

Show crontab:
```shell
crontab -l
```

See also:

- [Scheduling tasks with Cron - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/linux/usage/cron.md)


## Crontab logging

Uncomment `# cron.*` line in `/etc/rsyslog.conf` (eg. edit with `sudo vim /etc/rsyslog.conf`).

Show crontab log:

```shell
tail -f /var/log/cron.log
```

Or use output reirect in command:

```shell
/home/pi/cam-rpi-server/client-make-and-upload-image.sh >> /home/pi/cam-rpi-server/cron.log 2>&1
python /home/pi/cam-client/client-make-image.py >>  /home/pi/projects/cam-rpi-server/cron.log 2>&1
```

