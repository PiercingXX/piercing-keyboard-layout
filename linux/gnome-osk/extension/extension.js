// Piercing OSK Layout — registers a gresource containing piercing.json so
// GNOME Shell's on-screen keyboard finds a layout for the 'piercing' xkb
// input source. The stock osk-layouts bundle has no piercing.json, so
// registering an extra resource adds the layout without conflicting with
// (or replacing) any system file.
import Gio from 'gi://Gio';

import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

export default class PiercingOskExtension extends Extension {
    enable() {
        this._resource = Gio.Resource.load(`${this.path}/piercing-osk.gresource`);
        Gio.resources_register(this._resource);
    }

    disable() {
        Gio.resources_unregister(this._resource);
        this._resource = null;
    }
}
