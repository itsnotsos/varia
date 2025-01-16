import gi
from stringstorage import gettext as _
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
import time
import threading

def window_create_content(self):
    self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

    self.total_download_speed_label = Gtk.Label(label=self.total_download_speed)

    header_show_sidebar_button = Gtk.Button()
    header_show_sidebar_button.add_css_class('flat')
    header_show_sidebar_button.set_icon_name("sidebar-show-symbolic")
    header_show_sidebar_button.connect("clicked", toggle_sidebar_overlay, self)
    header_show_sidebar_button.set_halign(Gtk.Align.START)

    self.header_show_sidebar_button_revealer = Gtk.Revealer()
    self.header_show_sidebar_button_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
    self.header_show_sidebar_button_revealer.set_child(header_show_sidebar_button)

    self.header_pause_content = Adw.ButtonContent()
    self.header_pause_content.set_icon_name("media-playback-pause-symbolic")
    self.header_pause_content.set_label(_("Pause All"))
    self.header_pause_button = Gtk.Button()
    self.header_pause_button.set_sensitive(False)
    self.header_pause_button.set_child(self.header_pause_content)
    self.header_pause_button.connect("clicked", lambda button: self.pause_all(self.header_pause_content))
    
    header_expanding_box_1 = Gtk.Box()
    header_expanding_box_1.set_hexpand(True)
    header_expanding_box_2 = Gtk.Box()
    header_expanding_box_2.set_hexpand(True)
    
    header_box.append(header_expanding_box_1)
    header_box.append(self.total_download_speed_label)
    header_box.append(header_expanding_box_2)
    header_box.append(self.header_pause_button)

    self.header_bar = Adw.HeaderBar()
    self.header_bar.add_css_class('flat')
    self.header_bar.pack_start(self.header_show_sidebar_button_revealer)
    self.header_bar.set_title_widget(header_box)
    self.content_box.append(self.header_bar)

    status_page_begin_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    status_page_begin_button_box.append(Gtk.Image.new_from_icon_name("sidebar-show-symbolic"))
    status_page_begin_button_box.append(Gtk.Label(label=_("Show Menu")))

    status_page_begin_button = Gtk.Button(child=status_page_begin_button_box)
    status_page_begin_button.set_halign(Gtk.Align.CENTER)
    status_page_begin_button.add_css_class("pill")
    status_page_begin_button.add_css_class("suggested-action")
    status_page_begin_button.connect("clicked", toggle_sidebar_overlay, self)

    self.status_page_begin_button_revealer = Gtk.Revealer()
    self.status_page_begin_button_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
    self.status_page_begin_button_revealer.set_child(status_page_begin_button)
    
    self.status_page_widget = Adw.StatusPage(icon_name="io.github.giantpinkrobots.varia-symbolic")
    self.status_page_widget.set_hexpand(True)
    self.status_page_widget.set_vexpand(True)
    self.status_page_widget.set_child(self.status_page_begin_button_revealer)
    
    self.download_list_box = Gtk.Box()
    self.download_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    self.download_list.set_margin_start(6)
    self.download_list.set_margin_end(6)
    self.download_list.set_margin_bottom(6)
    self.download_list.set_margin_top(1)
    self.download_list_box.set_hexpand(True)
    self.download_list_box.set_vexpand(True)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_child(self.download_list)

    self.content_root_overlay = Gtk.Overlay()
    self.content_root_overlay.set_child(self.download_list_box)
    self.content_root_overlay.add_overlay(self.status_page_widget)

    self.download_list_box.append(scrolled_window)
    self.content_box.append(self.content_root_overlay)
    self.overlay_split_view.set_content(self.content_box)

    self.total_download_speed_calculator_thread = threading.Thread(target=self.total_download_speed_get, args=(self.downloads, self.total_download_speed_label))
    self.total_download_speed_calculator_thread.start()

    #self.check_download_status_thread = threading.Thread(target=lambda: check_download_status(self))
    #self.check_download_status_thread.start()

"""
def check_download_status(self):
    while (self.terminating == False):
        i = 0
        for download_thread in self.downloads:
            try:
                if (download_thread.download):
                    if (download_thread.mode == "regular" and download_thread.is_torrent and download_thread.is_metadata) == False and \
                        (download_thread.mode == "regular" and download_thread.download.is_complete == 1) or \
                        ( (download_thread.mode == "video" and download_thread.video_status == "finished") and \
                        ( (download_thread.video_download_combined == False) or ( (download_thread.video_download_combined == True and download_thread.video_download_stage == 0) == False) ) ):
                        
                        
                        GLib.idle_add(download_thread.set_complete)

                    elif (download_thread.mode == "regular" and (download_thread.download.status == "error") or (download_thread.download.status == "removed")) or (download_thread.mode == "video" and download_thread.video_status == "error"):
                        download_thread.cancelled = True

                        if (download_thread.download.error_code == "24"):
                            download_thread.speed_label.set_text(_("Authorization failed."))

                        else:
                            download_thread.speed_label.set_text(_("An error occurred:") + " " + str(download_thread.download.error_code))
                        download_thread.stop(False)

                        GLib.idle_add(download_thread.pause_button.set_visible, False)
                        self.filter_download_list("no", self.applied_filter)
            except:
                pass
            i += 1
        
        time.sleep(0.5)
"""

def toggle_sidebar_overlay(button, self):
    if self.overlay_split_view.get_show_sidebar() == False:
        self.overlay_split_view.set_collapsed(True)
        self.overlay_split_view.set_show_sidebar(True)
    else:
        self.overlay_split_view.set_show_sidebar(False)

def check_for_all_paused(self):
    all_paused = True

    for download_item in self.downloads.copy():
        if (download_item.download) and (download_item.is_alive()) and (download_item.return_is_paused() == False):
            all_paused = False

    if all_paused:
        self.all_paused = True
        self.header_pause_content.set_icon_name("media-playback-start-symbolic")
        self.header_pause_content.set_label(_("Resume All"))
        self.header_pause_button.set_sensitive(True)
    
    else:
        self.header_pause_content.set_icon_name("media-playback-pause-symbolic")
        self.header_pause_content.set_label(_("Pause All"))
        self.header_pause_button.set_sensitive(True)
