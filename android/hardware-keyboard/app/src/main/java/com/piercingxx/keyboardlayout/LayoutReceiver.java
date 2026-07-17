package com.piercingxx.keyboardlayout;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/** No-op receiver: the system only reads the KEYBOARD_LAYOUTS meta-data. */
public class LayoutReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
    }
}
