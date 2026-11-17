#ifndef EEZ_LVGL_UI_SCREENS_H
#define EEZ_LVGL_UI_SCREENS_H

#include <lvgl.h>

#ifdef __cplusplus
extern "C" {
#endif

// Screens

enum ScreensEnum {
    _SCREEN_ID_FIRST = 1,
    SCREEN_ID_MAIN = 1,
    SCREEN_ID_DATA = 2,
    _SCREEN_ID_LAST = 2
};

typedef struct _objects_t {
    lv_obj_t *main;
    lv_obj_t *data;
    lv_obj_t *deploy;
    lv_obj_t *force_stop;
    lv_obj_t *depressurize;
    lv_obj_t *home;
    lv_obj_t *graphs;
    lv_obj_t *errors;
    lv_obj_t *obj0;
    lv_obj_t *obj1;
    lv_obj_t *obj2;
    lv_obj_t *obj3;
    lv_obj_t *obj4;
    lv_obj_t *obj5;
    lv_obj_t *obj6;
    lv_obj_t *home_1;
    lv_obj_t *graphs_1;
    lv_obj_t *errors_1;
    lv_obj_t *obj7;
    lv_obj_t *deploy_1;
    lv_obj_t *force_stop_1;
    lv_obj_t *depressurize_1;
} objects_t;

extern objects_t objects;

void create_screen_main();
void tick_screen_main();

void create_screen_data();
void tick_screen_data();

void tick_screen_by_id(enum ScreensEnum screenId);
void tick_screen(int screen_index);

void create_screens();

#ifdef __cplusplus
}
#endif

#endif /*EEZ_LVGL_UI_SCREENS_H*/