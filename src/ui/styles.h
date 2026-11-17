#ifndef EEZ_LVGL_UI_STYLES_H
#define EEZ_LVGL_UI_STYLES_H

#include <lvgl.h>

#ifdef __cplusplus
extern "C" {
#endif

// Style: title
lv_style_t *get_style_title_MAIN_DEFAULT();
void add_style_title(lv_obj_t *obj);
void remove_style_title(lv_obj_t *obj);

// Style: text
lv_style_t *get_style_text_MAIN_DEFAULT();
void add_style_text(lv_obj_t *obj);
void remove_style_text(lv_obj_t *obj);

// Style: background
lv_style_t *get_style_background_MAIN_DEFAULT();
void add_style_background(lv_obj_t *obj);
void remove_style_background(lv_obj_t *obj);

// Style: panel
lv_style_t *get_style_panel_MAIN_DEFAULT();
void add_style_panel(lv_obj_t *obj);
void remove_style_panel(lv_obj_t *obj);

// Style: big buttons
lv_style_t *get_style_big_buttons_MAIN_DEFAULT();
void add_style_big_buttons(lv_obj_t *obj);
void remove_style_big_buttons(lv_obj_t *obj);

// Style: button
lv_style_t *get_style_button_MAIN_DEFAULT();
void add_style_button(lv_obj_t *obj);
void remove_style_button(lv_obj_t *obj);

#ifdef __cplusplus
}
#endif

#endif /*EEZ_LVGL_UI_STYLES_H*/