import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango
from stringstorage import gettext as _
from download.thread import DownloadThread
import json

def on_download_clicked(button, self, entry, downloadname, download, mode, video_options, paused, dir):
    if isinstance(entry, str):
        url = entry
    else:
        url = entry.get_text()
        entry.set_text("")
    
    if isinstance(video_options, str):
        video_options = json.loads(video_options)

    if url:
        download_item = create_actionrow(self, url)
        download_thread = DownloadThread(self, url, download_item, downloadname, download, mode, video_options, paused, dir)
        download_item.download_thread = download_thread
        self.downloads.append(download_thread)
        download_thread.start()

def create_actionrow(self, filename):
    download_item = Adw.Bin()

    download_item.add_css_class('card')

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box_1.set_margin_bottom(10)

    box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box_2.set_margin_start(10)
    box_2.set_margin_end(10)
    box_2.set_margin_top(10)
    box_2.set_margin_bottom(10)

    download_item.set_child(box_2)

    filename_label = Gtk.Label(label=filename)
    filename_label.set_ellipsize(Pango.EllipsizeMode.END)
    filename_label.set_halign(Gtk.Align.START)
    box.append(filename_label)

    progress_bar = Gtk.ProgressBar()

    speed_label = Gtk.Label()
    speed_label.set_ellipsize(Pango.EllipsizeMode.END)
    speed_label.set_halign(Gtk.Align.START)
    speed_label.add_css_class("dim-label")
    box.append(speed_label)

    button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    button_box.set_margin_start(10)

    pause_button_icon = Gtk.Image.new()
    pause_button_icon.set_from_icon_name("media-playback-pause-symbolic")

    pause_button = Gtk.Button.new()
    pause_button.set_child(pause_button_icon)
    pause_button.set_valign(Gtk.Align.CENTER)
    pause_button.add_css_class("circular")
    pause_button.connect("clicked", on_pause_clicked, self, pause_button, download_item, False, True)

    button_box.append(pause_button)

    stop_button = Gtk.Button.new_from_icon_name("process-stop-symbolic")
    stop_button.set_valign(Gtk.Align.CENTER)
    stop_button.add_css_class("circular")
    stop_button.add_css_class("destructive-action")
    stop_button.connect("clicked", on_stop_clicked, self, download_item)
    button_box.append(stop_button)

    box_1.append(box)

    box_1_expanding_box = Gtk.Box()
    Gtk.Widget.set_hexpand(box_1_expanding_box, True)
    box_1.append(box_1_expanding_box)

    box_1.append(button_box)
    box_2.append(box_1)
    box_2.append(progress_bar)

    self.download_list.prepend(download_item)

    self.content_root_overlay.remove_overlay(self.status_page_widget)

    download_item.progress_bar = progress_bar
    download_item.speed_label = speed_label
    download_item.pause_button = pause_button
    download_item.filename_label = filename_label

    return download_item

def on_pause_clicked(button, self, pause_button, download_item, force_pause, run_pause_function):

    if download_item.download_thread.return_is_paused() and force_pause == False:
        download_item.download_thread.resume()

    else:
        if run_pause_function:
            download_item.download_thread.pause(False)

def on_stop_clicked(button, self, download_item):
    download_item.download_thread.stop(download_item.download_thread.is_complete == False)
    self.download_list.remove(download_item)
    if (download_item.download_thread in self.downloads):
        self.downloads.remove(download_item.download_thread)
    if (self.download_list.get_first_child() == None):
        self.header_pause_content.set_icon_name("media-playback-pause-symbolic")
        self.header_pause_content.set_label(_("Pause All"))
        self.header_pause_button.set_sensitive(False)
        self.content_root_overlay.add_overlay(self.status_page_widget)
    download_item.download_thread = None
    download_item = None
