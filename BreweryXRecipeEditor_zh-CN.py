import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from PIL import Image, ImageTk

###############################################
# Custom dialog for entering a drink name with
# Minecraft color-code insertion buttons.
###############################################
class NameDialog:
    def __init__(self, parent, GoodOrBad):
        self.top = tk.Toplevel(parent)
        self.top.title("输入饮料名称")  # 标题汉化
        self.top.grab_set()
        self.result = None

        # 根据类型显示不同提示文本
        prompt_text = {
            "bad": "请输入坏品质变种名称:",     # 坏品质汉化
            "regular": "请输入普通品质名称:",    # 普通品质汉化
            "good": "请输入好品质变种名称:"      # 好品质汉化
        }.get(GoodOrBad, "请输入饮料名称:")      # 默认提示

        tk.Label(self.top, text=prompt_text).pack(pady=5)  # 统一提示文本逻辑
        self.entry = tk.Entry(self.top, width=40)
        self.entry.pack(pady=5)

        # 颜色代码按钮框架
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=5)

        # Minecraft 颜色代码（保留原始代码格式）
        self.color_codes = [
            ("&0", "#000000"),
            # ... 其他颜色代码保持不变 ...
            ("&u", "#9A5CC6")
        ]

        # 生成颜色代码按钮（保留功能，仅调整间距）
        for code, color in self.color_codes:
            btn = tk.Button(btn_frame,
                            text=code,
                            fg=color,
                            command=lambda c=code: self.insert_color_code(c))
            btn.pack(side="left", padx=1)  # 缩小按钮间距

        # 自定义颜色按钮汉化
        custom_btn = tk.Button(btn_frame,
                               text="自定义",  # "Custom" 汉化
                               command=self.custom_color_code)
        custom_btn.pack(side="left", padx=2)

        # 操作按钮框架
        action_frame = tk.Frame(self.top)
        action_frame.pack(pady=5)

        # 确定按钮汉化
        ok_btn = tk.Button(action_frame,
                           text="确定",  # "OK" 汉化
                           command=self.on_ok)
        ok_btn.pack(side="left", padx=10)

        # 取消按钮汉化
        cancel_btn = tk.Button(action_frame,
                               text="取消",  # "Cancel" 汉化
                               command=self.top.destroy)
        cancel_btn.pack(side="left", padx=10)

    def insert_color_code(self, code):
        """插入颜色代码（功能不变）"""
        self.entry.insert(tk.INSERT, code)

    def custom_color_code(self):
        """自定义颜色选择（添加中文标题）"""
        _, color = colorchooser.askcolor(title="选择自定义颜色")  # 添加中文标题
        if color:  # 添加非空判断
            self.insert_color_code("&" + color.lstrip('#'))  # 修复颜色格式

    def on_ok(self):
        """确认操作（逻辑不变）"""
        self.result = self.entry.get()
        self.top.destroy()

###############################################################
# 基于Treeview的材料选择器（带搜索功能）
###############################################################
class ItemSelector(ttk.Frame):
    def __init__(self, parent, items, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.items = items
        self.select_callback = select_callback
        self.image_cache = {}

        # 搜索框
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(fill="x", padx=5, pady=5)

        # 树形视图
        self.tree = ttk.Treeview(self, columns=("名称",), show="tree")  # 列名汉化
        self.tree.heading("#0", text="物品名称")  # 添加中文列标题
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # 滚动条
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.tree.configure(yscrollcommand=vsb.set)

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.populate_tree(self.items)

    def populate_tree(self, items):
        """填充物品列表"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in items:
            name = item.get("name", "未知物品")  # 默认值汉化
            item_id = item.get("id", "")
            self.tree.insert("", "end", iid=item_id, text=name)

    def update_filter(self, *args):
        """更新搜索过滤器"""
        term = self.search_var.get().lower()
        filtered = [item for item in self.items if term in item.get("name", "").lower()]
        self.populate_tree(filtered)

    def on_item_double_click(self, event):
        """处理双击选择事件"""
        selected_id = self.tree.focus()
        if not selected_id:
            return
        selected_item = next((item for item in self.items if item.get("id") == selected_id), None)
        if selected_item:
            # 汉化数量输入对话框
            item_name = selected_item.get("name", "未知物品")
            amount = simpledialog.askinteger(
                "输入数量",
                f"请输入{item_name}的数量：",  # 提示信息汉化
                parent=self.parent,
                minvalue=1,
                maxvalue=64
            )
            if amount:
                self.select_callback(selected_item, amount)

###############################################################
# 药水效果选择器（带中文效果名称映射）
###############################################################
class PotionEffectSelector(ttk.Frame):
    # 药水效果中英文对照表
    EFFECT_TRANSLATIONS = {
        "ABSORPTION": "伤害吸收",
        "BAD_OMEN": "不祥之兆",
        "BLINDNESS": "失明",
        "CONDUIT_POWER": "潮涌能量",
        "DARKNESS": "黑暗",
        "DOLPHINS_GRACE": "海豚的恩惠",
        "FIRE_RESISTANCE": "防火",
        "GLOWING": "发光",
        "HASTE": "急迫",
        "HEALTH_BOOST": "生命提升",
        "HERO_OF_THE_VILLAGE": "村庄英雄",
        "HUNGER": "饥饿",
        "INFESTED": "虫蚀",
        "INSTANT_DAMAGE": "瞬间伤害",
        "INSTANT_HEALTH": "瞬间治疗",
        "INVISIBILITY": "隐身",
        "JUMP_BOOST": "跳跃提升",
        "LEVITATION": "飘浮",
        "LUCK": "幸运",
        "MINING_FATIGUE": "挖掘疲劳",
        "NAUSEA": "反胃",
        "NIGHT_VISION": "夜视",
        "OOZING": "渗出",
        "POISON": "中毒",
        "RAID_OMEN": "袭击征兆",
        "REGENERATION": "生命恢复",
        "RESISTANCE": "抗性提升",
        "SATURATION": "饱和",
        "SLOW_FALLING": "缓降",
        "SLOWNESS": "缓慢",
        "SPEED": "速度",
        "STRENGTH": "力量",
        "TRIAL_OMEN": "试炼征兆",
        "UNLUCK": "霉运",
        "WATER_BREATHING": "水下呼吸",
        "WEAKNESS": "虚弱",
        "WEAVING": "织网",
        "WIND_CHARGED": "风袭",
        "WITHER": "凋零"
    }

    def __init__(self, parent, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.select_callback = select_callback

        # 初始化带中文显示的效果列表
        self.effects = list(self.EFFECT_TRANSLATIONS.keys())

        # 搜索框
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(fill="x", padx=5, pady=5)

        # 树形视图
        self.tree = ttk.Treeview(self, columns=("效果",), show="tree")
        self.tree.heading("#0", text="药水效果")  # 添加中文列标题
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # 滚动条
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.populate_tree(self.effects)

    def load_image_for_item(self, effect):
        """加载效果图标（保持原功能）"""
        image_path = os.path.join(os.path.dirname(__file__), "effects", f"{effect.lower()}.png")
        if os.path.exists(image_path):
            try:
                return ImageTk.PhotoImage(Image.open(image_path))
            except Exception as e:
                print(f"加载{effect}图标错误: {e}")  # 错误信息汉化

    def populate_tree(self, effects):
        """填充效果列表（显示中文名称）"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for effect in effects:
            display_name = self.EFFECT_TRANSLATIONS.get(effect, effect)
            image = self.load_image_for_item(effect)
            if image:
                self.tree.insert("", "end", iid=effect, text=display_name, image=image)
            else:
                self.tree.insert("", "end", iid=effect, text=display_name)

    def update_filter(self, *args):
        """更新搜索过滤器（支持中英文搜索）"""
        term = self.search_var.get().lower()
        filtered = [
            e for e in self.effects
            if term in e.lower() or term in self.EFFECT_TRANSLATIONS[e].lower()
        ]
        self.populate_tree(filtered)

    def on_item_double_click(self, event):
        """处理双击选择事件"""
        selected_id = self.tree.focus()
        if not selected_id:
            return

        # 获取中文效果名称
        zh_effect = self.tree.item(selected_id, "text")
        en_effect = selected_id  # 保持英文标识符

        # 汉化输入对话框
        level = simpledialog.askstring(
            "效果等级",
            f"请输入{zh_effect}的等级：\n（例如：2 或 1-3，1为最低效果，3为最高效果）",  # 示例汉化
            initialvalue="1"
        )
        if level is None:
            return

        duration = simpledialog.askstring(
            "持续时间",
            f"请输入{zh_effect}的持续时间（秒）：\n（例如：10 或 10-50，10秒为最短，50秒为最长）",  # 示例汉化
            initialvalue="30"
        )
        if duration is None:
            return

        self.select_callback(en_effect, level, duration)

###############################################################
# 主应用程序类
###############################################################
class BreweryRecipeGenerator():
    def __init__(self, master):
        self.master = master
        master.title("酿酒配方生成器")
        master.geometry("800x600")
        self.master.attributes("-topmost", True)  # 保持窗口置顶

        def delayed_topmost():
            self.master.attributes("-topmost", True)
        self.master.after(100, delayed_topmost)

        # 加载标题图片
        header_path = os.path.join(os.path.dirname(__file__), '2FA', "ses.jpg")
        if os.path.exists(header_path):
            try:
                header_img = Image.open(header_path)
                header_photo = ImageTk.PhotoImage(header_img)
                header_label = tk.Label(master, image=header_photo)
                header_label.image = header_photo  # 保持图片引用
                header_label.pack(pady=5)
            except Exception as e:
                print(f"标题图片加载失败: {e}")

        # 主功能按钮
        ttk.Style().configure("TButton", padding=6, relief="flat")
        btn_frame = ttk.Frame(master)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="新建饮品配方",
                   command=self.new_drink_recipe).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="新建坩埚配方",
                   command=self.new_cauldron_recipe).grid(row=0, column=1, padx=10)

        self.ingredients = []  # 存储配方成分

    def load_items_from_json(self, file_path, prefix):
        """从JSON文件加载物品数据"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, item in enumerate(data):
                    item["id"] = f"{prefix}_{item.get('id', idx)}"  # 生成唯一ID
                return data
        except Exception as e:
            messagebox.showerror("加载错误",
                                 f"文件加载失败: {os.path.basename(file_path)}\n错误详情: {str(e)}")
            return []

    def load_all_items(self):
        """加载全部物品数据"""
        return [
            *self.load_items_from_json("items.json", "r1"),
            *self.load_items_from_json("blocks.json", "r2")
        ]

    def new_drink_recipe(self):
        """创建新饮品配方"""
        # 获取三个品质的名称
        quality_types = {
            "bad": "坏品质",
            "regular": "普通品质",
            "good": "好品质"
        }
        names = {}

        for qtype, label in quality_types.items():
            dialog = NameDialog(self.master, qtype)
            self.master.wait_window(dialog.top)
            if not dialog.result or not dialog.result.strip():
                messagebox.showerror("输入错误", f"{label}名称不能为空！")
                return
            names[qtype] = dialog.result

        # 初始化组件
        self._init_components()
        all_items = self.load_all_items()

        # 创建配方编辑窗口
        edit_win = tk.Toplevel(self.master)
        edit_win.title("配方编辑器 - " + names["regular"])
        edit_win.geometry("900x700")

        # 使用标签页容器
        notebook = ttk.Notebook(edit_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 材料选择标签页
        self._create_ingredient_tab(notebook, all_items)
        # 药水效果标签页
        self._create_effect_tab(notebook)
        # 物品描述标签页
        self._create_lore_tab(notebook)
        # 服务器指令标签页
        self._create_server_cmd_tab(notebook)
        # 玩家指令标签页
        self._create_player_cmd_tab(notebook)

        # 确认区域
        confirm_frame = ttk.Frame(edit_win)
        confirm_frame.pack(pady=10)

        ttk.Button(confirm_frame, text="生成配方",
                   command=lambda: self._finalize_recipe(edit_win, names),
                   style="Accent.TButton").pack(side="left", padx=20)

        ttk.Button(confirm_frame, text="取消",
                   command=edit_win.destroy).pack(side="right", padx=20)

    def _init_components(self):
        """初始化所有组件"""
        self.ingredients = []
        self.potion_effects = []
        self.lore_text_widgets = []
        self.command_text_widgets = []
        self.playercommand_text_widgets = []

    def _create_ingredient_tab(self, parent, items):
        """创建材料选择标签页"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="材料配方")

        # 材料选择器
        def on_select(item, amount):
            self.ingredients.append(f"  - {item['name']}/{amount}")
            messagebox.showinfo("添加成功", f"已添加 {item['name']} x{amount}")

        selector = ItemSelector(tab, items, on_select)
        selector.pack(fill="both", expand=True, padx=10, pady=10)

        # 自定义物品按钮
        ttk.Button(tab, text="添加自定义物品",
                   command=self._add_custom_ingredient).pack(pady=5)

    def _add_custom_ingredient(self):
        """添加自定义材料"""
        input_str = simpledialog.askstring("自定义材料",
                                           "请输入完整物品ID和数量\n格式示例: minecraft:apple/3")
        if input_str:
            try:
                item_id, amount = input_str.rsplit("/", 1)
                if not amount.isdigit():
                    raise ValueError
                self.ingredients.append(f"  - {item_id}/{amount}")
                messagebox.showinfo("添加成功", f"已添加自定义材料: {item_id}")
            except (ValueError, TypeError):
                messagebox.showerror("格式错误", "请输入正确格式：物品ID/数量")

    def _create_effect_tab(self, parent):
        """创建药水效果标签页"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="药水效果")

        def on_effect_select(effect, level, duration):
            self.potion_effects.append(f"  - {effect}/{level}/{duration}")
            messagebox.showinfo("效果添加", f"已添加效果: {effect} Lv{level} ({duration}秒)")

        selector = PotionEffectSelector(tab, on_effect_select)
        selector.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_lore_tab(self, parent):
        """创建物品描述标签页"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="物品描述")

        # 描述输入框
        scroll = tk.Scrollbar(tab)
        text = tk.Text(tab, height=10, wrap="word", yscrollcommand=scroll.set)
        scroll.config(command=text.yview)

        scroll.pack(side="right", fill="y")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        self.lore_text_widgets.append(text)

        # 格式说明按钮
        ttk.Button(tab, text="格式说明",
                   command=lambda: messagebox.showinfo("描述格式",
                                                       "可使用以下格式：\n"
                                                       "固定显示文本\n"
                                                       "+ 坏品质时显示\n"
                                                       "++ 普通品质时显示\n"
                                                       "+++ 好品质时显示")).pack(pady=5)

    def _create_server_cmd_tab(self, parent):
        """创建服务器指令标签页"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="服务器指令")

        # 指令输入框
        scroll = tk.Scrollbar(tab)
        text = tk.Text(tab, height=10, wrap="word", yscrollcommand=scroll.set)
        scroll.config(command=text.yview)

        scroll.pack(side="right", fill="y")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        self.command_text_widgets.append(text)

        # 示例说明
        ttk.Button(tab, text="示例查看",
                   command=lambda: messagebox.showinfo("指令示例",
                                                       "指令示例：\n"
                                                       "say 全局公告\n"
                                                       "+ kill @a[tag=bad]\n"
                                                       "++ effect give @a regeneration 60")).pack(pady=5)

    def _create_player_cmd_tab(self, parent):
        """创建玩家指令标签页"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="玩家指令")

        # 指令输入框
        scroll = tk.Scrollbar(tab)
        text = tk.Text(tab, height=10, wrap="word", yscrollcommand=scroll.set)
        scroll.config(command=text.yview)

        scroll.pack(side="right", fill="y")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        self.playercommand_text_widgets.append(text)

        ttk.Button(tab, text="示例查看",
                   command=lambda: messagebox.showinfo("指令示例",
                                                       "示例指令：\n"
                                                       "tellraw @s {\"text\":\"饮酒提示\"}\n"
                                                       "++ tp @s ~ ~5 ~")).pack(pady=5)

    def _finalize_recipe(self, edit_win, names):
        """最终生成配方"""
        recipe = f"name: '{names['bad']}/{names['regular']}/{names['good']}'\n"

        # 基础属性
        recipe += self._get_basic_properties()
        # 材料列表
        recipe += "ingredients:\n" + "\n".join(self.ingredients) + "\n"
        # 药水效果
        recipe += self._get_effects()
        # 描述文本
        recipe += self._get_lore_text()
        # 指令部分
        recipe += self._get_commands()
        # 其他属性
        recipe += self._get_extra_properties()

        # 显示结果窗口
        result_win = tk.Toplevel(self.master)
        result_win.title("生成配方 - " + names["regular"])
        result_win.geometry("800x600")

        text_frame = ttk.Frame(result_win)
        text_frame.pack(fill="both", expand=True, padx=20, pady=20)

        text = tk.Text(text_frame, wrap="word", font=("Consolas", 10))
        scroll = ttk.Scrollbar(text_frame, command=text.yview)
        text.config(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        text.pack(fill="both", expand=True)

        text.insert("end", recipe)
        text.config(state="disabled")

        # 操作按钮
        btn_frame = ttk.Frame(result_win)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="复制配方",
                   command=lambda: self._copy_to_clipboard(recipe)).pack(side="left", padx=20)
        ttk.Button(btn_frame, text="关闭窗口",
                   command=result_win.destroy).pack(side="right", padx=20)

        edit_win.destroy()

    def _get_basic_properties(self):
        """获取基础属性"""
        properties = ""

        # 烹饪时间
        if cook_time := simpledialog.askinteger("烹饪时间", "请输入烹饪时间（分钟）", minvalue=1):
            properties += f"cookingtime: {cook_time}\n"

        # 蒸馏设置
        if distill_runs := simpledialog.askinteger("蒸馏次数", "请输入蒸馏次数（0表示不需要）", minvalue=0):
            properties += f"distillruns: {distill_runs}\n"
            if distill_time := simpledialog.askinteger("蒸馏时间", "每次蒸馏所需时间（分钟）", minvalue=1):
                properties += f"distilltime: {distill_time}\n"

        # 颜色选择
        _, hex_color = colorchooser.askcolor(title="选择饮品颜色")
        if hex_color:
            properties += f"color: '{hex_color.lstrip('#')}'\n"

        return properties

    def _get_effects(self):
        """处理药水效果"""
        if not self.potion_effects:
            return ""
        return "effects:\n" + "\n".join(self.potion_effects) + "\n"

    def _get_lore_text(self):
        """处理描述文本"""
        if not self.lore_text_widgets:
            return ""

        lore_lines = []
        for widget in self.lore_text_widgets:
            if text := widget.get("1.0", "end-1c"):
                lore_lines.extend(f"  - {line}" for line in text.split("\n"))

        return "lore:\n" + "\n".join(lore_lines) + "\n" if lore_lines else ""

    def _get_commands(self):
        """处理指令部分"""
        commands = ""

        # 服务器指令
        if server_cmds := self._process_cmd_widgets(self.command_text_widgets):
            commands += "servercommands:\n" + server_cmds

        # 玩家指令
        if player_cmds := self._process_cmd_widgets(self.playercommand_text_widgets):
            commands += "playercommands:\n" + player_cmds

        return commands

    def _process_cmd_widgets(self, widgets):
        """处理指令输入框"""
        cmd_lines = []
        for widget in widgets:
            if text := widget.get("1.0", "end-1c"):
                cmd_lines.extend(f"  - {line}" for line in text.split("\n"))
        return "\n".join(cmd_lines) + "\n" if cmd_lines else ""

    def _get_extra_properties(self):
        """获取额外属性"""
        properties = ""

        # 难度等级
        if difficulty := simpledialog.askinteger("酿造难度", "请输入难度等级（1-10）", minvalue=1, maxvalue=10):
            properties += f"difficulty: {difficulty}\n"

        # 酒精含量
        if alcohol := simpledialog.askinteger("酒精含量", "酒精浓度（-100 至 100）", minvalue=-100, maxvalue=100):
            properties += f"alcohol: {alcohol}\n"

        # 陈酿设置
        if wood_type := simpledialog.askstring("木桶类型", "请输入陈酿所需木桶类型（留空表示任意）"):
            properties += f"wood: {wood_type}\n"
        if age_time := simpledialog.askinteger("陈酿时间", "请输入陈酿年份", minvalue=0):
            properties += f"age: {age_time}\n"

        # 附加效果
        if glint := messagebox.askyesno("发光效果", "是否添加物品发光效果？"):
            properties += "glint: true\n"

        # 饮用提示
        if msg := simpledialog.askstring("饮用提示", "请输入饮用后显示的聊天栏消息"):
            properties += f"drinkmessage: {msg}\n"
        if title := simpledialog.askstring("饮用标题", "请输入饮用后显示的大标题（留空不设置）"):
            properties += f"drinktitle: {title}\n"

        return properties

    def _copy_to_clipboard(self, content):
        """复制到剪贴板"""
        self.master.clipboard_clear()
        self.master.clipboard_append(content)
        messagebox.showinfo("复制成功", "配方已复制到剪贴板！")

    def new_cauldron_recipe(self):
        """新建坩埚配方（功能占位）"""
        messagebox.showinfo("功能开发中",
                            "坩埚配方功能正在开发中，敬请期待！\n当前版本暂不支持此功能。")

###############################################################
# 运行应用程序
###############################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = BreweryRecipeGenerator(root)
    root.mainloop()