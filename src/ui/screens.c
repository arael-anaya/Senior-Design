#include <string.h>

#include "screens.h"
#include "images.h"
#include "fonts.h"
#include "actions.h"
#include "vars.h"
#include "styles.h"
#include "ui.h"

#include <string.h>

objects_t objects;

static const char *screen_names[] = { "Main", "data" };
static const char *object_names[] = { "main", "data", "deploy", "force_stop", "depressurize", "home", "graphs", "errors", "obj0", "obj1", "obj2", "obj3", "obj4", "obj5", "obj6", "home_1", "graphs_1", "errors_1", "obj7", "deploy_1", "force_stop_1", "depressurize_1" };

//
// Event handlers
//

lv_obj_t *tick_value_change_obj;

//
// Screens
//

void create_screen_main() {
    void *flowState = getFlowState(0, 0);
    (void)flowState;
    lv_obj_t *obj = lv_obj_create(0);
    objects.main = obj;
    lv_obj_set_pos(obj, 0, 0);
    lv_obj_set_size(obj, 320, 240);
    {
        lv_obj_t *parent_obj = obj;
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 0, 0);
            lv_obj_set_size(obj, 320, 240);
            add_style_background(obj);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 14, 12);
            lv_obj_set_size(obj, 152, 45);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 20, 29);
            lv_obj_set_size(obj, 141, LV_SIZE_CONTENT);
            add_style_title(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Deployable xRAD Radiators");
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 14, 68);
            lv_obj_set_size(obj, 290, 95);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 30, 89);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "State:");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 30, 121);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Latch:");
        }
        {
            // Deploy
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.deploy = obj;
            lv_obj_set_pos(obj, 14, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "DEPLOY");
                }
            }
        }
        {
            // Force Stop
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.force_stop = obj;
            lv_obj_set_pos(obj, 117, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 1);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "FORCE\n  STOP");
                }
            }
        }
        {
            // Depressurize
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.depressurize = obj;
            lv_obj_set_pos(obj, 220, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, " RELEASE\nPRESSURE");
                }
            }
        }
        {
            // Home
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.home = obj;
            lv_obj_set_pos(obj, 181, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Main");
                }
            }
        }
        {
            // Graphs
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.graphs = obj;
            lv_obj_set_pos(obj, 225, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Data");
                }
            }
        }
        {
            // Errors
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.errors = obj;
            lv_obj_set_pos(obj, 268, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_opa(obj, 40, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_opa(obj, 30, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_outline_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_shadow_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_shadow_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    objects.obj0 = obj;
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Errors");
                }
            }
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj1 = obj;
            lv_obj_set_pos(obj, 98, 121);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Closed");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj2 = obj;
            lv_obj_set_pos(obj, 98, 89);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xe0e0e0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Stowed");
        }
    }
    
    tick_screen_main();
}

void tick_screen_main() {
    void *flowState = getFlowState(0, 0);
    (void)flowState;
}

void create_screen_data() {
    void *flowState = getFlowState(0, 1);
    (void)flowState;
    lv_obj_t *obj = lv_obj_create(0);
    objects.data = obj;
    lv_obj_set_pos(obj, 0, 0);
    lv_obj_set_size(obj, 320, 240);
    {
        lv_obj_t *parent_obj = obj;
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 0, 0);
            lv_obj_set_size(obj, 320, 240);
            add_style_background(obj);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 14, 68);
            lv_obj_set_size(obj, 152, 97);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_arc_create(parent_obj);
            lv_obj_set_pos(obj, 28, 97);
            lv_obj_set_size(obj, 89, 91);
            lv_arc_set_value(obj, 25);
            lv_obj_set_style_arc_width(obj, 12, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_transform_scale_x(obj, 128, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_transform_scale_y(obj, 128, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 181, 119);
            lv_obj_set_size(obj, 123, 46);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 181, 68);
            lv_obj_set_size(obj, 123, 46);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 192, 73);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Acceleration");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 217, 123);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Angle");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj3 = obj;
            lv_obj_set_pos(obj, 24, 139);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xe0e0e0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_14, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "14.7 psi");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj4 = obj;
            lv_obj_set_pos(obj, 102, 139);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xe0e0e0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_14, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "14.7 psi");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj5 = obj;
            lv_obj_set_pos(obj, 211, 94);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xe0e0e0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_14, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "0 m/s^2");
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            objects.obj6 = obj;
            lv_obj_set_pos(obj, 203, 144);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_color(obj, lv_color_hex(0xe0e0e0), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_14, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "0 degrees");
        }
        {
            lv_obj_t *obj = lv_obj_create(parent_obj);
            lv_obj_set_pos(obj, 14, 12);
            lv_obj_set_size(obj, 152, 45);
            add_style_panel(obj);
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 20, 29);
            lv_obj_set_size(obj, 141, LV_SIZE_CONTENT);
            add_style_title(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Deployable xRAD Radiators");
        }
        {
            // Home_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.home_1 = obj;
            lv_obj_set_pos(obj, 181, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Main");
                }
            }
        }
        {
            // Graphs_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.graphs_1 = obj;
            lv_obj_set_pos(obj, 225, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Data");
                }
            }
        }
        {
            // Errors_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.errors_1 = obj;
            lv_obj_set_pos(obj, 268, 12);
            lv_obj_set_size(obj, 36, 45);
            add_style_big_buttons(obj);
            lv_obj_set_style_bg_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_bg_opa(obj, 40, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_border_opa(obj, 30, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_outline_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_shadow_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_shadow_opa(obj, 0, LV_PART_MAIN | LV_STATE_DEFAULT);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    objects.obj7 = obj;
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_color(obj, lv_color_hex(0xc8373b), LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_10, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "Errors");
                }
            }
        }
        {
            // Deploy_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.deploy_1 = obj;
            lv_obj_set_pos(obj, 14, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 0);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "DEPLOY");
                }
            }
        }
        {
            // Force Stop_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.force_stop_1 = obj;
            lv_obj_set_pos(obj, 117, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 2);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, "FORCE\n  STOP");
                }
            }
        }
        {
            // Depressurize_1
            lv_obj_t *obj = lv_button_create(parent_obj);
            objects.depressurize_1 = obj;
            lv_obj_set_pos(obj, 220, 174);
            lv_obj_set_size(obj, 84, 43);
            add_style_big_buttons(obj);
            {
                lv_obj_t *parent_obj = obj;
                {
                    lv_obj_t *obj = lv_label_create(parent_obj);
                    lv_obj_set_pos(obj, 0, 1);
                    lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
                    add_style_button(obj);
                    lv_obj_set_style_align(obj, LV_ALIGN_CENTER, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_obj_set_style_text_font(obj, &lv_font_montserrat_12, LV_PART_MAIN | LV_STATE_DEFAULT);
                    lv_label_set_text_static(obj, " RELEASE\nPRESSURE");
                }
            }
        }
        {
            lv_obj_t *obj = lv_label_create(parent_obj);
            lv_obj_set_pos(obj, 55, 73);
            lv_obj_set_size(obj, LV_SIZE_CONTENT, LV_SIZE_CONTENT);
            add_style_text(obj);
            lv_obj_set_style_text_font(obj, &lv_font_montserrat_16, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_label_set_text_static(obj, "Pressure");
        }
        {
            lv_obj_t *obj = lv_arc_create(parent_obj);
            lv_obj_set_pos(obj, 104, 97);
            lv_obj_set_size(obj, 89, 91);
            lv_arc_set_value(obj, 25);
            lv_obj_set_style_arc_width(obj, 12, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_transform_scale_x(obj, 128, LV_PART_MAIN | LV_STATE_DEFAULT);
            lv_obj_set_style_transform_scale_y(obj, 128, LV_PART_MAIN | LV_STATE_DEFAULT);
        }
    }
    
    tick_screen_data();
}

void tick_screen_data() {
    void *flowState = getFlowState(0, 1);
    (void)flowState;
}

typedef void (*tick_screen_func_t)();
tick_screen_func_t tick_screen_funcs[] = {
    tick_screen_main,
    tick_screen_data,
};
void tick_screen(int screen_index) {
    if (screen_index >= 0 && screen_index < 2) {
        tick_screen_funcs[screen_index]();
    }
}
void tick_screen_by_id(enum ScreensEnum screenId) {
    tick_screen(screenId - 1);
}

//
// Styles
//

static const char *style_names[] = { "title", "text", "background", "panel", "big buttons", "button" };

extern void add_style(lv_obj_t *obj, int32_t styleIndex);
extern void remove_style(lv_obj_t *obj, int32_t styleIndex);

//
// Fonts
//

ext_font_desc_t fonts[] = {
#if LV_FONT_MONTSERRAT_8
    { "MONTSERRAT_8", &lv_font_montserrat_8 },
#endif
#if LV_FONT_MONTSERRAT_10
    { "MONTSERRAT_10", &lv_font_montserrat_10 },
#endif
#if LV_FONT_MONTSERRAT_12
    { "MONTSERRAT_12", &lv_font_montserrat_12 },
#endif
#if LV_FONT_MONTSERRAT_14
    { "MONTSERRAT_14", &lv_font_montserrat_14 },
#endif
#if LV_FONT_MONTSERRAT_16
    { "MONTSERRAT_16", &lv_font_montserrat_16 },
#endif
#if LV_FONT_MONTSERRAT_18
    { "MONTSERRAT_18", &lv_font_montserrat_18 },
#endif
#if LV_FONT_MONTSERRAT_20
    { "MONTSERRAT_20", &lv_font_montserrat_20 },
#endif
#if LV_FONT_MONTSERRAT_22
    { "MONTSERRAT_22", &lv_font_montserrat_22 },
#endif
#if LV_FONT_MONTSERRAT_24
    { "MONTSERRAT_24", &lv_font_montserrat_24 },
#endif
#if LV_FONT_MONTSERRAT_26
    { "MONTSERRAT_26", &lv_font_montserrat_26 },
#endif
#if LV_FONT_MONTSERRAT_28
    { "MONTSERRAT_28", &lv_font_montserrat_28 },
#endif
#if LV_FONT_MONTSERRAT_30
    { "MONTSERRAT_30", &lv_font_montserrat_30 },
#endif
#if LV_FONT_MONTSERRAT_32
    { "MONTSERRAT_32", &lv_font_montserrat_32 },
#endif
#if LV_FONT_MONTSERRAT_34
    { "MONTSERRAT_34", &lv_font_montserrat_34 },
#endif
#if LV_FONT_MONTSERRAT_36
    { "MONTSERRAT_36", &lv_font_montserrat_36 },
#endif
#if LV_FONT_MONTSERRAT_38
    { "MONTSERRAT_38", &lv_font_montserrat_38 },
#endif
#if LV_FONT_MONTSERRAT_40
    { "MONTSERRAT_40", &lv_font_montserrat_40 },
#endif
#if LV_FONT_MONTSERRAT_42
    { "MONTSERRAT_42", &lv_font_montserrat_42 },
#endif
#if LV_FONT_MONTSERRAT_44
    { "MONTSERRAT_44", &lv_font_montserrat_44 },
#endif
#if LV_FONT_MONTSERRAT_46
    { "MONTSERRAT_46", &lv_font_montserrat_46 },
#endif
#if LV_FONT_MONTSERRAT_48
    { "MONTSERRAT_48", &lv_font_montserrat_48 },
#endif
};

//
//
//

void create_screens() {
    // Initialize styles
    eez_flow_init_styles(add_style, remove_style);
    eez_flow_init_style_names(style_names, sizeof(style_names) / sizeof(const char *));

eez_flow_init_fonts(fonts, sizeof(fonts) / sizeof(ext_font_desc_t));

// Set default LVGL theme
    lv_display_t *dispp = lv_display_get_default();
    lv_theme_t *theme = lv_theme_default_init(dispp, lv_palette_main(LV_PALETTE_BLUE), lv_palette_main(LV_PALETTE_RED), false, LV_FONT_DEFAULT);
    lv_display_set_theme(dispp, theme);
    
    // Initialize screens
    eez_flow_init_screen_names(screen_names, sizeof(screen_names) / sizeof(const char *));
    eez_flow_init_object_names(object_names, sizeof(object_names) / sizeof(const char *));
    
    // Create screens
    create_screen_main();
    create_screen_data();
}