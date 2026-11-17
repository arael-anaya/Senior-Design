#include "styles.h"
#include "images.h"
#include "fonts.h"

#include "ui.h"
#include "screens.h"

//
// Style: title
//

void init_style_title_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_text_font(style, &lv_font_montserrat_30);
    lv_style_set_text_color(style, lv_color_hex(0xffffff));
};

lv_style_t *get_style_title_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_title_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_title(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_title_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_title(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_title_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
// Style: text
//

void init_style_text_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_text_font(style, &lv_font_montserrat_18);
    lv_style_set_text_color(style, lv_color_hex(0x869695));
};

lv_style_t *get_style_text_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_text_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_text(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_text_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_text(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_text_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
// Style: background
//

void init_style_background_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_bg_color(style, lv_color_hex(0x11191f));
};

lv_style_t *get_style_background_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_background_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_background(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_background_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_background(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_background_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
// Style: panel
//

void init_style_panel_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_bg_color(style, lv_color_hex(0x273340));
    lv_style_set_border_color(style, lv_color_hex(0x273340));
};

lv_style_t *get_style_panel_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_panel_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_panel(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_panel_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_panel(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_panel_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
// Style: big buttons
//

void init_style_big_buttons_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_text_font(style, &lv_font_montserrat_18);
    lv_style_set_bg_color(style, lv_color_hex(0x1b242e));
    lv_style_set_shadow_color(style, lv_color_hex(0x273340));
};

lv_style_t *get_style_big_buttons_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_big_buttons_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_big_buttons(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_big_buttons_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_big_buttons(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_big_buttons_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
// Style: button
//

void init_style_button_MAIN_DEFAULT(lv_style_t *style) {
    lv_style_set_align(style, LV_ALIGN_CENTER);
    lv_style_set_text_font(style, &lv_font_montserrat_18);
    lv_style_set_text_color(style, lv_color_hex(0x27c5ae));
};

lv_style_t *get_style_button_MAIN_DEFAULT() {
    static lv_style_t *style;
    if (!style) {
        style = (lv_style_t *)lv_malloc(sizeof(lv_style_t));
        lv_style_init(style);
        init_style_button_MAIN_DEFAULT(style);
    }
    return style;
};

void add_style_button(lv_obj_t *obj) {
    (void)obj;
    lv_obj_add_style(obj, get_style_button_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

void remove_style_button(lv_obj_t *obj) {
    (void)obj;
    lv_obj_remove_style(obj, get_style_button_MAIN_DEFAULT(), LV_PART_MAIN | LV_STATE_DEFAULT);
};

//
//
//

void add_style(lv_obj_t *obj, int32_t styleIndex) {
    typedef void (*AddStyleFunc)(lv_obj_t *obj);
    static const AddStyleFunc add_style_funcs[] = {
        add_style_title,
        add_style_text,
        add_style_background,
        add_style_panel,
        add_style_big_buttons,
        add_style_button,
    };
    add_style_funcs[styleIndex](obj);
}

void remove_style(lv_obj_t *obj, int32_t styleIndex) {
    typedef void (*RemoveStyleFunc)(lv_obj_t *obj);
    static const RemoveStyleFunc remove_style_funcs[] = {
        remove_style_title,
        remove_style_text,
        remove_style_background,
        remove_style_panel,
        remove_style_big_buttons,
        remove_style_button,
    };
    remove_style_funcs[styleIndex](obj);
}