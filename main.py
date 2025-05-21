import json
import os
import sys
import uuid
from pathlib import Path

from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel,
    QAbstractTableModel,
    QModelIndex,
    QSettings,
    QRegExp,
    QEvent,
    QLocale,
    QRegularExpression,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QStandardItemModel,
    QStandardItem,
    QSyntaxHighlighter,
    QTextCharFormat,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTableView,
    QComboBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QRadioButton,
    QSplitter,
    QHeaderView,
    QMenu,
    QAction,
    QStatusBar,
    QCompleter,
    QTextEdit,
    QToolBar,
    QToolButton,
    QMenuBar,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QInputDialog,
)

from jsonschema import Draft7Validator, ValidationError

# Set up paths relative to script location
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = SCRIPT_DIR.parent / "schemas"
DATA_DIR = SCRIPT_DIR.parent / "open-db"

# Ensure directories exist
SCHEMA_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Style definitions
LIGHT_STYLE = """
QWidget {
    background-color: #F0F0F0;
    color: #333333;
}
QMainWindow, QDialog {
    background-color: #F0F0F0;
}
QTableView {
    alternate-background-color: #E8E8E8;
    selection-background-color: #C2D8F2;
    selection-color: #333333;
    gridline-color: #CCCCCC;
}
QHeaderView::section {
    background-color: #E0E0E0;
    padding: 4px;
    border: 1px solid #CCCCCC;
}
QPushButton {
    background-color: #E8E8E8;
    border: 1px solid #BBBBBB;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #D0D0D0;
}
QPushButton:pressed {
    background-color: #B8B8B8;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: white;
    border: 1px solid #BBBBBB;
    border-radius: 3px;
    padding: 3px;
}
QMenuBar {
    background-color: #F0F0F0;
}
QMenuBar::item:selected {
    background-color: #CDCDCD;
}
QMenu {
    background-color: #F5F5F5;
    border: 1px solid #BBBBBB;
}
QMenu::item:selected {
    background-color: #D8D8D8;
}
QStatusBar {
    background-color: #E8E8E8;
}
QToolBar {
    background-color: #F0F0F0;
    border-bottom: 1px solid #CCCCCC;
}
QToolButton {
    background-color: transparent;
    border: none;
    padding: 6px;
}
QToolButton:hover {
    background-color: #D0D0D0;
    border-radius: 4px;
}
QTabWidget::pane {
    border: 1px solid #CCCCCC;
}
QTabBar::tab {
    background-color: #E0E0E0;
    border: 1px solid #CCCCCC;
    border-bottom-color: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 10px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #F0F0F0;
    border-bottom-color: #F0F0F0;
}
QTabBar::tab:hover:!selected {
    background-color: #D6D6D6;
}
"""

DARK_STYLE = """
QWidget {
    background-color: #2D2D2D;
    color: #E0E0E0;
}
QMainWindow, QDialog {
    background-color: #2D2D2D;
}
QTableView {
    alternate-background-color: #353535;
    selection-background-color: #3D7AB3;
    selection-color: #F0F0F0;
    gridline-color: #555555;
}
QHeaderView::section {
    background-color: #3A3A3A;
    padding: 4px;
    border: 1px solid #555555;
}
QPushButton {
    background-color: #444444;
    border: 1px solid #666666;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #555555;
}
QPushButton:pressed {
    background-color: #333333;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 3px;
    color: #E0E0E0;
}
QMenuBar {
    background-color: #2D2D2D;
}
QMenuBar::item:selected {
    background-color: #3A3A3A;
}
QMenu {
    background-color: #2D2D2D;
    border: 1px solid #555555;
}
QMenu::item:selected {
    background-color: #3D7AB3;
}
QStatusBar {
    background-color: #333333;
}
QToolBar {
    background-color: #2D2D2D;
    border-bottom: 1px solid #444444;
}
QToolButton {
    background-color: transparent;
    border: none;
    padding: 6px;
}
QToolButton:hover {
    background-color: #444444;
    border-radius: 4px;
}
QTabWidget::pane {
    border: 1px solid #555555;
}
QTabBar::tab {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    border-bottom-color: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 10px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #2D2D2D;
    border-bottom-color: #2D2D2D;
}
QTabBar::tab:hover:!selected {
    background-color: #444444;
}
QTextEdit {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    color: #E0E0E0;
}
QListWidget {
    background-color: #3A3A3A;
    border: 1px solid #555555;
    color: #E0E0E0;
}
QCheckBox {
    color: #E0E0E0;
}
QGroupBox {
    border: 1px solid #555555;
    border-radius: 4px;
    margin-top: 1ex;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 3px;
}
"""

class ArrayFieldButton(QPushButton):
    """Custom button for array fields with an "Edit..." label"""
    
    def __init__(self, array_data=None, item_type="string", parent=None):
        super().__init__("Edit...", parent)
        self.array_data = array_data or []
        self.item_type = item_type
        self.clicked.connect(self.open_editor)
        self.update_summary()
        
    def open_editor(self):
        """Open the array editor dialog"""
        dialog = ArrayEditorDialog(self.array_data, self.item_type, self)
        if dialog.exec_() == QDialog.Accepted:
            self.array_data = dialog.get_items()
            self.update_summary()
            
    def update_summary(self):
        """Update the button text with a summary of the array"""
        if not self.array_data:
            self.setText("Edit... (Empty)")
        else:
            self.setText(f"Edit... ({len(self.array_data)} items)")
            
    def get_array_data(self):
        """Get the current array data"""
        return self.array_data


class ChangeTrackingLineEdit(QLineEdit):
    """A LineEdit that tracks changes and highlights when modified"""
    
    def __init__(self, original_value="", parent=None):
        super().__init__(parent)
        self.original_value = str(original_value) if original_value is not None else ""
        self.setText(self.original_value)
        self.textChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
    def check_changed(self):
        """Check if the current text differs from the original value"""
        if self.text() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = str(value) if value is not None else ""
        self.check_changed()


class ChangeTrackingSpinBox(QSpinBox):
    """A SpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0, parent=None):
        super().__init__(parent)
        self.original_value = int(original_value) if original_value is not None else 0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if self.value() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = int(value) if value is not None else 0
        self.check_changed()

class SmartNumberSpinBox(QDoubleSpinBox):
    """A spin box that only shows decimal places when they're non-zero"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDecimals(10)  # Support up to 10 decimal places to avoid truncation
        self.setLocale(QLocale(QLocale.C))  # Disable locale-based formatting
        
        # Store the actual value to preserve precision
        self._actual_value = 0.0
        
        # Connect value changed signal
        self.valueChanged.connect(self._on_value_changed)
        
    def _on_value_changed(self, value):
        """Handle value changed event"""
        self._actual_value = value
    
    def textFromValue(self, value):
        """Convert value to text, removing trailing zeros but preserving precision"""
        # First, get the full precision string representation
        text = str(value)
        
        # If it's an integer value (X.0), convert to integer string
        if value == int(value):
            return str(int(value))
            
        # Otherwise, for decimal values, remove trailing zeros but keep the decimal point
        if '.' in text:
            return text.rstrip('0').rstrip('.') if text.endswith('.0') else text.rstrip('0')
            
        return text
        
    def valueFromText(self, text):
        """Parse value from text, handling both dots and commas as decimal separators"""
        # Replace comma with dot for decimal separator
        text = text.replace(',', '.')
        
        try:
            # Handle scientific notation
            if 'e' in text.lower():
                return float(text)
                
            # Parse as float
            return float(text)
        except ValueError:
            return 0.0



class ChangeTrackingSmartNumberSpinBox(SmartNumberSpinBox):
    """A SmartNumberSpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0.0, parent=None):
        super().__init__(parent)
        self.original_value = float(original_value) if original_value is not None else 0.0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if self.value() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = float(value) if value is not None else 0.0
        self.check_changed()

class BigNumberSpinBox(SmartNumberSpinBox):
    """
    A spin box that supports extremely large numbers beyond the standard Qt limits
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set to the maximum supported by Qt's QDoubleSpinBox
        self.setRange(-sys.float_info.max, sys.float_info.max)
        
        # For values that exceed Qt's display capabilities, we'll use scientific notation
        self.setSingleStep(1)  # Default step size
        self.setStepType(QDoubleSpinBox.AdaptiveDecimalStepType)
    
    def textFromValue(self, value):
        """Format numbers with full precision, only removing trailing zeros"""
        # Use scientific notation for extremely large numbers to prevent display issues
        if abs(value) > 1e12:  # For values above a trillion
            return f"{value:.10e}"  # Scientific notation with high precision
        
        # For standard numbers, use the parent class implementation
        # which already handles removing trailing zeros correctly
        return super().textFromValue(value)
        
    def setValue(self, value):
        """Set the value with full precision"""
        self._actual_value = value  # Store the exact value
        super().setValue(value)     # Update the displayed value
        
    def value(self):
        """Return the actual value with full precision"""
        return self._actual_value


class ChangeTrackingBigNumberSpinBox(BigNumberSpinBox):
    """A BigNumberSpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0.0, parent=None):
        super().__init__(parent)
        self.original_value = float(original_value) if original_value is not None else 0.0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if abs(self.value() - self.original_value) > 1e-10:  # Use small epsilon for float comparison
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = float(value) if value is not None else 0.0
        self.check_changed()


class ChangeTrackingComboBox(QComboBox):
    """A ComboBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value="", parent=None):
        super().__init__(parent)
        self.original_value = str(original_value) if original_value is not None else ""
        self.currentTextChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
    def check_changed(self):
        """Check if the current text differs from the original value"""
        if self.currentText() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = str(value) if value is not None else ""
        # Find and set the index for this value
        index = self.findText(self.original_value)
        if index >= 0:
            self.setCurrentIndex(index)
        self.check_changed()


class ChangeTrackingCheckBox(QCheckBox):
    """A CheckBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=False, parent=None):
        super().__init__(parent)
        self.original_value = bool(original_value) if original_value is not None else False
        self.setChecked(self.original_value)
        self.stateChanged.connect(self.check_changed)
        
        # Style for changed state - for checkbox we need to style the text since the box itself is hard to style
        self.original_style = self.styleSheet()
        self.changed_style = "color: #806000; font-weight: bold;"  # Dark yellow text, bold
        
    def check_changed(self):
        """Check if the current state differs from the original value"""
        if self.isChecked() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = bool(value) if value is not None else False
        self.setChecked(self.original_value)
        self.check_changed()


class ChangeTrackingArrayButton(ArrayFieldButton):
    """An ArrayFieldButton that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=None, item_type="string", parent=None):
        super().__init__(original_value, item_type, parent)
        self.original_value = original_value or []
        
        # Make a deep copy to avoid reference issues
        import copy
        self.original_value = copy.deepcopy(self.original_value)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFFFC0; color: black;"  # Light yellow background with black text
        
        # Check after initialization
        self.check_changed()
        
    def check_changed(self):
        """Check if the current array data differs from the original value"""
        changed = False
        
        # Different length means definitely changed
        if len(self.array_data) != len(self.original_value):
            changed = True
        else:
            # Compare each item
            for i, item in enumerate(self.array_data):
                if i >= len(self.original_value) or item != self.original_value[i]:
                    changed = True
                    break
                    
        if changed:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
    
    def set_array_data(self, data):
        """Override to track changes"""
        super().array_data = data
        self.update_summary()
        self.check_changed()
    
    def open_editor(self):
        """Override to track changes after editing"""
        dialog = ArrayEditorDialog(self.array_data, self.item_type, self)
        if dialog.exec_() == QDialog.Accepted:
            self.array_data = dialog.get_items()
            self.update_summary()
            self.check_changed()
            
    def set_original_value(self, value):
        """Set a new original value"""
        import copy
        self.original_value = copy.deepcopy(value) if value is not None else []
        self.check_changed()

class ChangeTrackingLineEdit(QLineEdit):
    """A LineEdit that tracks changes and highlights when modified"""
    
    def __init__(self, original_value="", parent=None):
        super().__init__(parent)
        self.original_value = str(original_value) if original_value is not None else ""
        self.setText(self.original_value)
        self.textChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
    def check_changed(self):
        """Check if the current text differs from the original value"""
        if self.text() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = str(value) if value is not None else ""
        self.check_changed()


class ChangeTrackingSpinBox(QSpinBox):
    """A SpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0, parent=None):
        super().__init__(parent)
        self.original_value = int(original_value) if original_value is not None else 0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if self.value() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = int(value) if value is not None else 0
        self.check_changed()


class ChangeTrackingSmartNumberSpinBox(SmartNumberSpinBox):
    """A SmartNumberSpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0.0, parent=None):
        super().__init__(parent)
        self.original_value = float(original_value) if original_value is not None else 0.0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if self.value() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = float(value) if value is not None else 0.0
        self.check_changed()


class ChangeTrackingBigNumberSpinBox(BigNumberSpinBox):
    """A BigNumberSpinBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=0.0, parent=None):
        super().__init__(parent)
        self.original_value = float(original_value) if original_value is not None else 0.0
        self.setValue(self.original_value)
        self.valueChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
    def check_changed(self):
        """Check if the current value differs from the original value"""
        if abs(self.value() - self.original_value) > 1e-10:  # Use small epsilon for float comparison
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = float(value) if value is not None else 0.0
        self.check_changed()


class ChangeTrackingComboBox(QComboBox):
    """A ComboBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value="", parent=None):
        super().__init__(parent)
        self.original_value = str(original_value) if original_value is not None else ""
        self.currentTextChanged.connect(self.check_changed)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
    def check_changed(self):
        """Check if the current text differs from the original value"""
        if self.currentText() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = str(value) if value is not None else ""
        # Find and set the index for this value
        index = self.findText(self.original_value)
        if index >= 0:
            self.setCurrentIndex(index)
        self.check_changed()


class ChangeTrackingCheckBox(QCheckBox):
    """A CheckBox that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=False, parent=None):
        super().__init__(parent)
        self.original_value = bool(original_value) if original_value is not None else False
        self.setChecked(self.original_value)
        self.stateChanged.connect(self.check_changed)
        
        # Style for changed state - for checkbox we use font weight and color
        self.original_style = self.styleSheet()
        # Dark golden text that's still readable in both light and dark themes
        self.changed_style = "color: #806000; font-weight: bold;"
        
    def check_changed(self):
        """Check if the current state differs from the original value"""
        if self.isChecked() != self.original_value:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
            
    def set_original_value(self, value):
        """Set a new original value"""
        self.original_value = bool(value) if value is not None else False
        self.setChecked(self.original_value)
        self.check_changed()


class ChangeTrackingArrayButton(ArrayFieldButton):
    """An ArrayFieldButton that tracks changes and highlights when modified"""
    
    def __init__(self, original_value=None, item_type="string", parent=None):
        super().__init__(original_value, item_type, parent)
        self.original_value = original_value or []
        
        # Make a deep copy to avoid reference issues
        import copy
        self.original_value = copy.deepcopy(self.original_value)
        
        # Style for changed state
        self.original_style = self.styleSheet()
        self.changed_style = "background-color: #FFDA80; color: black;"
        
        # Check after initialization
        self.check_changed()
        
    def check_changed(self):
        """Check if the current array data differs from the original value"""
        changed = False
        
        # Different length means definitely changed
        if len(self.array_data) != len(self.original_value):
            changed = True
        else:
            # Compare each item
            for i, item in enumerate(self.array_data):
                if i >= len(self.original_value) or item != self.original_value[i]:
                    changed = True
                    break
                    
        if changed:
            self.setStyleSheet(self.changed_style)
        else:
            self.setStyleSheet(self.original_style)
    
    def set_array_data(self, data):
        """Override to track changes"""
        super().array_data = data
        self.update_summary()
        self.check_changed()
    
    def open_editor(self):
        """Override to track changes after editing"""
        dialog = ArrayEditorDialog(self.array_data, self.item_type, self)
        if dialog.exec_() == QDialog.Accepted:
            self.array_data = dialog.get_items()
            self.update_summary()
            self.check_changed()
            
    def set_original_value(self, value):
        """Set a new original value"""
        import copy
        self.original_value = copy.deepcopy(value) if value is not None else []
        self.check_changed()


class ThemedDialog(QDialog):
    """Base dialog class that automatically applies the current theme"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apply_dialog_theme()
        
        # Set dialog icon directly from scripts directory
        icon_path = str(SCRIPT_DIR / "favicon.png")
        self.setWindowIcon(QIcon(icon_path))
        
        # Connect to show event to apply theme when dialog becomes visible
        self.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        """Event filter to catch show events"""
        if obj is self and event.type() == QEvent.Show:
            # Apply theme when dialog is shown (ensures title bar is themed)
            self.apply_dialog_theme()
        return super().eventFilter(obj, event)
        
    def apply_dialog_theme(self):
        """Apply the current theme to the dialog"""
        if not self.parent():
            return
            
        # Get the theme from the parent (main window)
        is_dark = getattr(self.parent(), 'is_dark_mode', False)
        
        # Apply theme to dialog title bar
        apply_window_theme(self, dark_mode=is_dark)
        
        # Apply the stylesheet
        if is_dark:
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)

class ArrayEditorDialog(ThemedDialog):
    """Dialog for editing array items"""
    
    def __init__(self, array_data=None, item_type="string", parent=None):
        super().__init__(parent)
        self.array_data = array_data or []
        self.item_type = item_type  # Type of items in the array (from schema)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Edit Array Items")
        self.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # List widget to display items
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        
        # Add existing items
        for item in self.array_data:
            self.list_widget.addItem(str(item))
            
        layout.addWidget(QLabel("Items:"))
        layout.addWidget(self.list_widget)
        
        # Input field for new items
        input_layout = QHBoxLayout()
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Enter new item...")
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)
        
        input_layout.addWidget(self.item_input)
        input_layout.addWidget(self.add_button)
        layout.addLayout(input_layout)
        
        # Buttons for editing
        button_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit Selected")
        self.remove_button = QPushButton("Remove Selected")
        self.move_up_button = QPushButton("Move Up")
        self.move_down_button = QPushButton("Move Down")
        
        self.edit_button.clicked.connect(self.edit_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.move_up_button.clicked.connect(self.move_item_up)
        self.move_down_button.clicked.connect(self.move_item_down)
        
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.move_up_button)
        button_layout.addWidget(self.move_down_button)
        layout.addLayout(button_layout)
        
        # Dialog buttons
        dialog_buttons = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        dialog_buttons.addWidget(self.ok_button)
        dialog_buttons.addWidget(self.cancel_button)
        layout.addLayout(dialog_buttons)
        
        self.setLayout(layout)
        
    def add_item(self):
        """Add a new item to the list"""
        item_text = self.item_input.text().strip()
        if not item_text:
            return
            
        # Add to list widget
        self.list_widget.addItem(item_text)
        
        # Clear input field
        self.item_input.clear()
        self.item_input.setFocus()
        
    def edit_item(self):
        """Edit the selected item"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Please select an item to edit.")
            return
            
        current_text = current_item.text()
        new_text, ok = QInputDialog.getText(
            self, "Edit Item", "Edit item value:", QLineEdit.Normal, current_text
        )
        
        if ok and new_text.strip():
            current_item.setText(new_text.strip())
            
    def remove_item(self):
        """Remove the selected item"""
        current_row = self.list_widget.currentRow()
        if current_row >= 0:
            self.list_widget.takeItem(current_row)
            
    def move_item_up(self):
        """Move the selected item up in the list"""
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            current_item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, current_item)
            self.list_widget.setCurrentRow(current_row - 1)
            
    def move_item_down(self):
        """Move the selected item down in the list"""
        current_row = self.list_widget.currentRow()
        if current_row >= 0 and current_row < self.list_widget.count() - 1:
            current_item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, current_item)
            self.list_widget.setCurrentRow(current_row + 1)
            
    def get_items(self):
        """Get all items from the list widget"""
        items = []
        for i in range(self.list_widget.count()):
            item_text = self.list_widget.item(i).text()
            
            # Convert to appropriate type based on schema
            if self.item_type == "string":
                items.append(item_text)
            elif self.item_type == "integer":
                try:
                    items.append(int(item_text))
                except ValueError:
                    items.append(0)  # Default value if conversion fails
            elif self.item_type == "number":
                try:
                    items.append(float(item_text))
                except ValueError:
                    items.append(0.0)  # Default value if conversion fails
            elif self.item_type == "boolean":
                items.append(item_text.lower() in ["true", "yes", "1"])
            else:
                items.append(item_text)
                
        return items


class NestedPropertyEditor(QWidget):
    """Widget for editing nested schema properties"""

    def __init__(self, property_name="", property_data=None, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.property_data = property_data or {"type": "object", "properties": {}}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Property name
        name_layout = QHBoxLayout()
        name_label = QLabel("Property Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.property_name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Property type (always object for nested properties)
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["object", "array"])
        current_type = "array" if self.property_data.get("type") == "array" else "object"
        if isinstance(self.property_data.get("type"), list):
            main_type = next((t for t in self.property_data["type"] if t != "null"), "object")
            current_type = "array" if main_type == "array" else "object"
        self.type_combo.setCurrentText(current_type)
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # Description
        description_layout = QHBoxLayout()
        description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.description_edit.setText(self.property_data.get("description", ""))
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)
        layout.addLayout(description_layout)

        # Required checkbox
        self.required_check = QCheckBox("Required")
        self.required_check.setChecked(False)  # This is managed by the parent dialog
        layout.addWidget(self.required_check)

        # Nullable checkbox
        self.nullable_check = QCheckBox("Nullable (allow null value)")

        # Check if the type is an array including "null"
        if isinstance(self.property_data.get("type"), list) and "null" in self.property_data["type"]:
            self.nullable_check.setChecked(True)
        else:
            self.nullable_check.setChecked(False)

        layout.addWidget(self.nullable_check)

        # Child properties section
        self.properties_group = QGroupBox("Child Properties")
        properties_layout = QVBoxLayout()

        # Tree view for nested properties
        self.properties_tree = QTreeWidget()
        self.properties_tree.setHeaderLabels(["Name", "Type", "Required"])
        self.properties_tree.setColumnWidth(0, 200)
        self.properties_tree.setColumnWidth(1, 150)
        self.properties_tree.setColumnWidth(2, 100)
        properties_layout.addWidget(self.properties_tree)

        # Buttons for managing properties
        buttons_layout = QHBoxLayout()
        self.add_prop_button = QPushButton("Add Property")
        self.edit_prop_button = QPushButton("Edit Property")
        self.remove_prop_button = QPushButton("Remove Property")

        self.add_prop_button.clicked.connect(self.add_property)
        self.edit_prop_button.clicked.connect(self.edit_property)
        self.remove_prop_button.clicked.connect(self.remove_property)

        buttons_layout.addWidget(self.add_prop_button)
        buttons_layout.addWidget(self.edit_prop_button)
        buttons_layout.addWidget(self.remove_prop_button)
        properties_layout.addLayout(buttons_layout)

        self.properties_group.setLayout(properties_layout)
        layout.addWidget(self.properties_group)

        # Array-specific options (for array type)
        self.array_group = QGroupBox("Array Options")
        array_layout = QVBoxLayout()

        # Items type for arrays
        items_layout = QHBoxLayout()
        items_label = QLabel("Items Type:")
        self.items_combo = QComboBox()
        self.items_combo.addItems(["string", "number", "integer", "boolean", "object"])

        if "items" in self.property_data and "type" in self.property_data["items"]:
            item_type = self.property_data["items"]["type"]
            if isinstance(item_type, list):
                # Handle case where item type is ["string", "null"]
                item_type = next((t for t in item_type if t != "null"), "string")
            self.items_combo.setCurrentText(item_type)

        items_layout.addWidget(items_label)
        items_layout.addWidget(self.items_combo)
        array_layout.addLayout(items_layout)

        # Items nullable checkbox
        self.items_nullable_check = QCheckBox("Items Nullable (allow null values in array)")

        # Check if the items type includes null
        items_nullable = False
        if "items" in self.property_data and "type" in self.property_data["items"]:
            if isinstance(self.property_data["items"]["type"], list) and "null" in self.property_data["items"]["type"]:
                items_nullable = True

        self.items_nullable_check.setChecked(items_nullable)
        array_layout.addWidget(self.items_nullable_check)

        # Complex items editor (for object items)
        self.items_object_button = QPushButton("Edit Object Items Schema")
        self.items_object_button.clicked.connect(self.edit_items_object_schema)
        array_layout.addWidget(self.items_object_button)

        self.array_group.setLayout(array_layout)
        layout.addWidget(self.array_group)

        # Set initial visibility based on type
        self.update_ui_for_type(self.type_combo.currentText())

        self.setLayout(layout)

        # Load existing properties
        self.load_properties()

    def on_type_changed(self, type_name):
        """Handle property type change"""
        self.update_ui_for_type(type_name)

    def update_ui_for_type(self, type_name):
        """Update UI elements based on property type"""
        if type_name == "object":
            self.properties_group.setVisible(True)
            self.array_group.setVisible(False)
        else:  # array
            self.properties_group.setVisible(False)
            self.array_group.setVisible(True)

    def load_properties(self):
        """Load existing properties into the tree view"""
        self.properties_tree.clear()

        if self.type_combo.currentText() == "object":
            properties = self.property_data.get("properties", {})
            required_fields = self.property_data.get("required", [])

            for prop_name, prop_data in properties.items():
                self.add_property_to_tree(prop_name, prop_data, prop_name in required_fields)

    def add_property_to_tree(self, name, data, required=False):
        """Add a property to the tree view"""
        item = QTreeWidgetItem()
        item.setText(0, name)

        # Handle type display (show "string | null" for nullable types)
        type_val = data.get("type", "string")
        if isinstance(type_val, list):
            if "null" in type_val:
                non_null_types = [t for t in type_val if t != "null"]
                type_display = " | ".join(non_null_types) + " | null"
            else:
                type_display = " | ".join(type_val)
        else:
            type_display = type_val

        item.setText(1, type_display)
        item.setText(2, "Yes" if required else "No")

        # Store the property data
        item.setData(0, Qt.UserRole, data)

        self.properties_tree.addTopLevelItem(item)

    def add_property(self):
        """Add a new child property"""
        dialog = PropertyEditorDialog("", {"type": "string"}, self)
        if dialog.exec_() == QDialog.Accepted:
            prop_name, prop_data, is_required = dialog.get_property_data()
            if prop_name:
                # Check for duplicate names
                for i in range(self.properties_tree.topLevelItemCount()):
                    item = self.properties_tree.topLevelItem(i)
                    if item.text(0) == prop_name:
                        QMessageBox.warning(
                            self,
                            "Duplicate Property",
                            f"Property '{prop_name}' already exists.",
                        )
                        return

                self.add_property_to_tree(prop_name, prop_data, is_required)

    def edit_property(self):
        """Edit selected child property"""
        selected_items = self.properties_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(
                self, "No Selection", "Please select a property to edit."
            )
            return

        item = selected_items[0]
        prop_name = item.text(0)
        prop_data = item.data(0, Qt.UserRole)
        is_required = item.text(2) == "Yes"

        dialog = PropertyEditorDialog(prop_name, prop_data, self)
        dialog.required_check.setChecked(is_required)

        if dialog.exec_() == QDialog.Accepted:
            new_name, new_data, new_required = dialog.get_property_data()
            if new_name:
                # Check for duplicate names if name changed
                if new_name != prop_name:
                    for i in range(self.properties_tree.topLevelItemCount()):
                        other_item = self.properties_tree.topLevelItem(i)
                        if other_item != item and other_item.text(0) == new_name:
                            QMessageBox.warning(
                                self,
                                "Duplicate Property",
                                f"Property '{new_name}' already exists.",
                            )
                            return

                # Update the item
                item.setText(0, new_name)

                # Update type display
                type_val = new_data.get("type", "string")
                if isinstance(type_val, list):
                    if "null" in type_val:
                        non_null_types = [t for t in type_val if t != "null"]
                        type_display = " | ".join(non_null_types) + " | null"
                    else:
                        type_display = " | ".join(type_val)
                else:
                    type_display = type_val

                item.setText(1, type_display)
                item.setText(2, "Yes" if new_required else "No")
                item.setData(0, Qt.UserRole, new_data)

    def remove_property(self):
        """Remove selected child property"""
        selected_items = self.properties_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(
                self, "No Selection", "Please select a property to remove."
            )
            return

        item = selected_items[0]
        prop_name = item.text(0)

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete property '{prop_name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        # Remove the item
        index = self.properties_tree.indexOfTopLevelItem(item)
        self.properties_tree.takeTopLevelItem(index)

    def edit_items_object_schema(self):
        """Edit the schema for object items in an array"""
        if self.type_combo.currentText() != "array":
            return

        if self.items_combo.currentText() != "object":
            QMessageBox.information(
                self, "Not an Object", "Items type must be 'object' to edit its schema."
            )
            return

        # Get current items schema or create a default one
        items_schema = self.property_data.get("items", {})
        if "properties" not in items_schema:
            items_schema["properties"] = {}

        # Create a dialog for editing the items schema
        dialog = NestedPropertyEditorDialog("items", items_schema, self)

        if dialog.exec_() == QDialog.Accepted:
            # Update the items schema
            _, items_schema, _ = dialog.get_property_data()
            self.property_data["items"] = items_schema

    def get_property_data(self):
        """Get the property data with nested properties"""
        property_name = self.name_edit.text().strip()
        if not property_name:
            return None, None, False

        # Basic property data
        property_type = self.type_combo.currentText()

        # Handle nullable types
        if self.nullable_check.isChecked():
            property_data = {"type": [property_type, "null"]}
        else:
            property_data = {"type": property_type}

        # Add description if provided
        description = self.description_edit.text().strip()
        if description:
            property_data["description"] = description

        if property_type == "object":
            # Add nested properties
            properties = {}
            required = []

            for i in range(self.properties_tree.topLevelItemCount()):
                item = self.properties_tree.topLevelItem(i)
                prop_name = item.text(0)
                prop_data = item.data(0, Qt.UserRole)
                is_required = item.text(2) == "Yes"

                properties[prop_name] = prop_data
                if is_required:
                    required.append(prop_name)

            property_data["properties"] = properties
            if required:
                property_data["required"] = required

        elif property_type == "array":
            # Add items type
            items_type = self.items_combo.currentText()

            # Handle nullable items
            if self.items_nullable_check.isChecked():
                property_data["items"] = {"type": [items_type, "null"]}
            else:
                property_data["items"] = {"type": items_type}

            # For object items, add any nested properties
            if items_type == "object" and "items" in self.property_data and "properties" in self.property_data["items"]:
                property_data["items"]["properties"] = self.property_data["items"]["properties"]
                if "required" in self.property_data["items"]:
                    property_data["items"]["required"] = self.property_data["items"]["required"]

        return property_name, property_data, self.required_check.isChecked()
    

class PropertyEditorDialog(ThemedDialog):
    """Dialog for editing a property with advanced options"""

    def __init__(self, property_name="", property_data=None, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.property_data = property_data or {"type": "string"}
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Edit Property")
        self.resize(500, 400)

        layout = QVBoxLayout()

        # Create property editor widget
        self.editor = PropertyEditorWidget(self.property_name, self.property_data, self)
        layout.addWidget(self.editor)

        # Add buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_property_data(self):
        """Get the property data from the editor"""
        return self.editor.get_property_data()


class NestedPropertyEditorDialog(ThemedDialog):
    """Dialog for editing nested properties"""

    def __init__(self, property_name="", property_data=None, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.property_data = property_data or {"type": "object", "properties": {}}
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Edit Nested Property")
        self.resize(700, 500)

        layout = QVBoxLayout()

        # Create nested property editor
        self.editor = NestedPropertyEditor(self.property_name, self.property_data, self)
        layout.addWidget(self.editor)

        # Add buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_property_data(self):
        """Get the property data from the editor"""
        return self.editor.get_property_data()
    

class PropertyEditorWidget(QWidget):
    """Widget for editing a single property in a schema"""

    def __init__(self, property_name="", property_data=None, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.property_data = property_data or {"type": "string"}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Property name
        name_layout = QHBoxLayout()
        name_label = QLabel("Property Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.property_name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Property type
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(
            ["string", "integer", "number", "boolean", "array", "object"]
        )

        # Handle type that could be a list like ["string", "null"]
        current_type = self.property_data.get("type", "string")
        if isinstance(current_type, list):
            # Filter out "null" to get the main type
            non_null_types = [t for t in current_type if t != "null"]
            if non_null_types:
                self.type_combo.setCurrentText(non_null_types[0])
            else:
                self.type_combo.setCurrentText("string")  # Default if only null
        else:
            self.type_combo.setCurrentText(current_type)

        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # Nullable checkbox (for allowing null values)
        self.nullable_check = QCheckBox("Nullable (allow null value)")

        # Check if the type is an array including "null"
        if isinstance(self.property_data.get("type"), list) and "null" in self.property_data["type"]:
            self.nullable_check.setChecked(True)
        else:
            self.nullable_check.setChecked(False)

        layout.addWidget(self.nullable_check)

        # Type-specific options
        self.type_options_group = QGroupBox("Type Options")
        self.type_options_layout = QVBoxLayout()
        self.type_options_group.setLayout(self.type_options_layout)
        layout.addWidget(self.type_options_group)

        # Update type-specific options
        self.update_type_options()

        # Description
        description_layout = QHBoxLayout()
        description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.description_edit.setText(self.property_data.get("description", ""))
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)
        layout.addLayout(description_layout)

        # Required checkbox
        self.required_check = QCheckBox("Required")
        self.required_check.setChecked(False)  # This is managed by the parent dialog
        layout.addWidget(self.required_check)

        # Add button for complex types (object, array)
        self.advanced_button = QPushButton("Advanced Configuration")
        self.advanced_button.clicked.connect(self.open_advanced_editor)
        self.advanced_button.setVisible(self.type_combo.currentText() in ["object", "array"])
        layout.addWidget(self.advanced_button)

        self.setLayout(layout)

    def on_type_changed(self, type_name):
        """Handle property type change"""
        self.property_data["type"] = type_name
        self.update_type_options()

        # Show/hide advanced button based on type
        self.advanced_button.setVisible(type_name in ["object", "array"])

        # Reset any object/array specific properties when changing types
        if type_name == "object" and "properties" not in self.property_data:
            self.property_data["properties"] = {}
        elif type_name == "array" and "items" not in self.property_data:
            self.property_data["items"] = {"type": "string"}

    def update_type_options(self):
        """Update type-specific options based on current type"""
        # Clear existing options
        for i in reversed(range(self.type_options_layout.count())):
            item = self.type_options_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.type_options_layout.removeItem(item)

        type_name = self.type_combo.currentText()

        if type_name == "string":
            # String options: format, enum, pattern, etc.
            format_layout = QHBoxLayout()
            format_label = QLabel("Format:")
            self.format_combo = QComboBox()
            self.format_combo.addItems(
                ["", "date-time", "date", "time", "email", "uuid", "uri", "hostname"]
            )
            self.format_combo.setCurrentText(self.property_data.get("format", ""))
            format_layout.addWidget(format_label)
            format_layout.addWidget(self.format_combo)
            self.type_options_layout.addLayout(format_layout)

            # Enum values
            enum_label = QLabel("Enum Values (comma-separated):")
            self.enum_edit = QLineEdit()
            if "enum" in self.property_data:
                self.enum_edit.setText(", ".join(self.property_data["enum"]))
            self.type_options_layout.addWidget(enum_label)
            self.type_options_layout.addWidget(self.enum_edit)

        elif type_name in ["integer", "number"]:
            # Numeric options: minimum, maximum, etc.
            min_layout = QHBoxLayout()
            min_label = QLabel("Minimum:")
            self.min_spin = QSpinBox() if type_name == "integer" else QDoubleSpinBox()
            self.min_spin.setRange(-999999999, 999999999)
            if "minimum" in self.property_data:
                self.min_spin.setValue(self.property_data["minimum"])
            min_layout.addWidget(min_label)
            min_layout.addWidget(self.min_spin)
            self.type_options_layout.addLayout(min_layout)

            max_layout = QHBoxLayout()
            max_label = QLabel("Maximum:")
            self.max_spin = QSpinBox() if type_name == "integer" else QDoubleSpinBox()
            self.max_spin.setRange(-999999999, 999999999)
            if "maximum" in self.property_data:
                self.max_spin.setValue(self.property_data["maximum"])
            max_layout.addWidget(max_label)
            max_layout.addWidget(self.max_spin)
            self.type_options_layout.addLayout(max_layout)

        elif type_name == "boolean":
            # Boolean options: default value
            default_layout = QHBoxLayout()
            default_label = QLabel("Default:")
            self.default_check = QCheckBox()
            self.default_check.setChecked(self.property_data.get("default", False))
            default_layout.addWidget(default_label)
            default_layout.addWidget(self.default_check)
            self.type_options_layout.addLayout(default_layout)

        elif type_name == "array":
            # Array options: items type
            items_layout = QHBoxLayout()
            items_label = QLabel("Items Type:")
            self.items_combo = QComboBox()
            self.items_combo.addItems(
                ["string", "integer", "number", "boolean", "object"]
            )

            # Handle items type that could be a list like ["string", "null"]
            if "items" in self.property_data:
                items_type = self.property_data["items"].get("type", "string")
                if isinstance(items_type, list):
                    # Filter out "null" to get the main type
                    non_null_types = [t for t in items_type if t != "null"]
                    if non_null_types:
                        self.items_combo.setCurrentText(non_null_types[0])
                    else:
                        self.items_combo.setCurrentText("string")
                else:
                    self.items_combo.setCurrentText(items_type)

            items_layout.addWidget(items_label)
            items_layout.addWidget(self.items_combo)
            self.type_options_layout.addLayout(items_layout)

            # Nullable items checkbox
            self.items_nullable_check = QCheckBox("Allow null items in array")

            # Check if items type includes null
            if "items" in self.property_data:
                items_type = self.property_data["items"].get("type", "string")
                self.items_nullable_check.setChecked(
                    isinstance(items_type, list) and "null" in items_type
                )

            self.type_options_layout.addWidget(self.items_nullable_check)

        elif type_name == "object":
            # Object options
            info_label = QLabel("Use 'Advanced Configuration' for nested properties")
            self.type_options_layout.addWidget(info_label)

    def open_advanced_editor(self):
        """Open advanced editor for object or array types"""
        type_name = self.type_combo.currentText()
        
        if type_name in ["object", "array"]:
            # Create a dialog with the nested property editor
            dialog = QDialog(self)
            dialog.setWindowTitle("Advanced Configuration")
            dialog.resize(700, 500)
            
            layout = QVBoxLayout()
            
            # Create nested property editor
            if type_name == "object":
                # Create a copy of our property data for the nested editor
                nested_data = dict(self.property_data)
                if "properties" not in nested_data:
                    nested_data["properties"] = {}
                
                nested_editor = NestedPropertyEditor(
                    self.name_edit.text().strip(), 
                    nested_data, 
                    dialog
                )
                nested_editor.name_edit.setEnabled(False)  # Don't allow changing the name
                layout.addWidget(nested_editor)
                
            elif type_name == "array":
                # For arrays, we'll edit the 'items' property if it's an object
                items_type = self.items_combo.currentText()
                
                if items_type == "object":
                    # Get or create the items schema
                    items_schema = self.property_data.get("items", {})
                    if "properties" not in items_schema:
                        items_schema["properties"] = {}
                    if "type" not in items_schema:
                        items_schema["type"] = "object"
                        
                    nested_editor = NestedPropertyEditor(
                        "items",
                        items_schema,
                        dialog
                    )
                    nested_editor.name_edit.setEnabled(False)  # Don't allow changing the name
                    layout.addWidget(nested_editor)
                else:
                    layout.addWidget(QLabel(f"Advanced configuration is only available for object items."))
                    layout.addWidget(QLabel(f"Current items type is: {items_type}"))
                    
            # Add buttons
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            cancel_button = QPushButton("Cancel")
            
            ok_button.clicked.connect(dialog.accept)
            cancel_button.clicked.connect(dialog.reject)
            
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            dialog.setLayout(layout)
            
            # Execute the dialog
            if dialog.exec_() == QDialog.Accepted and hasattr(nested_editor, "get_property_data"):
                # Update the property data from the nested editor
                _, updated_data, _ = nested_editor.get_property_data()
                
                if type_name == "object":
                    # Keep the original type (which might include null)
                    original_type = self.property_data.get("type", "object")
                    
                    # Update our property data, preserving the type
                    self.property_data.update(updated_data)
                    self.property_data["type"] = original_type
                    
                elif type_name == "array" and items_type == "object":
                    # For arrays, update just the items schema
                    if "items" not in self.property_data:
                        self.property_data["items"] = {}
                        
                    # Keep only the properties and required fields
                    if "properties" in updated_data:
                        self.property_data["items"]["properties"] = updated_data["properties"]
                    if "required" in updated_data:
                        self.property_data["items"]["required"] = updated_data["required"]
                    
                    # Make sure type is preserved
                    items_type_value = "object"
                    if self.items_nullable_check.isChecked():
                        self.property_data["items"]["type"] = ["object", "null"]
                    else:
                        self.property_data["items"]["type"] = "object"


class DataTableModel(QAbstractTableModel):
    """
    Model for displaying hardware component data in a table with support for nested fields
    """

    def __init__(self, data=None, headers=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._headers = headers or []
        self._validation_results = {}
        self._required_fields = []
        self._flattened_data = []
        self._flatten_data()

    def set_required_fields(self, required_fields):
        """Set which fields are required"""
        self._required_fields = required_fields

    def set_validation_results(self, validation_results):
        """Set validation results for entries"""
        self._validation_results = validation_results
        self.layoutChanged.emit()

    def _flatten_data(self):
        """Flatten nested data for display in table"""
        self._flattened_data = []

        for entry in self._data:
            flattened = {}

            # Always include ID
            flattened["opendb_id"] = entry.get("opendb_id", "")

            # Flatten other fields
            for field in self._headers:
                if field == "opendb_id":
                    continue

                if "." in field:
                    # Handle nested fields with dot notation (e.g. "metadata.name")
                    parts = field.split(".")
                    value = entry
                    for part in parts:
                        if isinstance(value, dict) and part in value:
                            value = value[part]
                        else:
                            value = ""
                            break
                    flattened[field] = value
                else:
                    # Handle top-level fields
                    flattened[field] = entry.get(field, "")

            self._flattened_data.append(flattened)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            row, col = index.row(), index.column()
            if row >= len(self._flattened_data) or col >= len(self._headers):
                return None

            field = self._headers[col]

            # Return the value, ensuring proper string conversion with encoding handling
            value = self._flattened_data[row].get(field, "")

            # Handle different types for display
            if value is None:
                return "null"
            elif isinstance(value, dict):
                return "{...}"  # Show indicator for objects
            elif isinstance(value, list):
                return f"[{len(value)} items]"  # Show count for arrays
            else:
                # Convert any non-string values to string, preserving Unicode characters
                return str(value)

        elif role == Qt.BackgroundRole:
            row, col = index.row(), index.column()
            if row >= len(self._flattened_data) or col >= len(self._headers):
                return None

            item_id = self._flattened_data[row].get("opendb_id")
            field = self._headers[col]

            # No validation results available
            if not self._validation_results:
                return None

            # Check validation issues for this specific field
            if item_id in self._validation_results:
                result = self._validation_results[item_id]

                # Missing required field
                if field in result.get("missing_required", []):
                    return QColor(255, 200, 200)  # Light red

                # Type mismatch
                for mismatch in result.get("type_mismatches", []):
                    mismatch_field = mismatch["field"]
                    # Check both exact match and field being part of a path
                    if mismatch_field == field or mismatch_field.startswith(f"{field}."):
                        return QColor(255, 230, 200)  # Light orange

                # Missing optional field
                if field in result.get("missing_optional", []):
                    return QColor(255, 255, 200)  # Light yellow

        elif role == Qt.FontRole:
            row, col = index.row(), index.column()
            if row >= len(self._flattened_data) or col >= len(self._headers):
                return None

            field = self._headers[col]
            font = QFont()

            # Make required fields bold
            if field in self._required_fields:
                font.setBold(True)
                return font

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and section < len(self._headers):
                return self._headers[section]
            else:
                return str(section + 1)
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._flattened_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def refresh_data(self, data):
        """Update the model with new data"""
        self.beginResetModel()
        self._data = data
        self._flatten_data()
        self.endResetModel()

    def get_row_data(self, row):
        """Get the data for a specific row"""
        if 0 <= row < len(self._data):
            return self._data[row].copy()
        return None


class AdvancedFilterProxyModel(QSortFilterProxyModel):
    """
    Enhanced filter proxy model with support for different search modes:
    - Contains (partial match, case insensitive)
    - Exact (full match, case sensitive)
    - Starts With
    - Ends With
    - Regular Expression
    """
    
    # Search mode constants
    CONTAINS = 0
    EXACT = 1
    STARTS_WITH = 2
    ENDS_WITH = 3
    REGEX = 4
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_mode = self.CONTAINS
        self.search_columns = []  # If empty, search all columns
        
    def setSearchMode(self, mode):
        """Set the search mode"""
        self.search_mode = mode
        self.invalidateFilter()
        
    def setSearchColumns(self, columns):
        """Set which columns to search in (empty list means all columns)"""
        self.search_columns = columns
        self.invalidateFilter()
        
    def filterAcceptsRow(self, source_row, source_parent):
        """Override to implement custom filtering logic"""
        # If filter is empty, accept all rows
        if not self.filterRegExp().pattern():
            return True
            
        # If specific columns are set, only search in those columns
        if self.search_columns:
            columns_to_search = self.search_columns
        else:
            # Search all columns
            columns_to_search = range(self.sourceModel().columnCount())
            
        for column in columns_to_search:
            index = self.sourceModel().index(source_row, column, source_parent)
            if not index.isValid():
                continue
                
            data = self.sourceModel().data(index, Qt.DisplayRole)
            if data is None:
                continue
                
            text = str(data)
            search_term = self.filterRegExp().pattern()
            
            # Apply the appropriate search mode
            if self.search_mode == self.CONTAINS:
                if search_term.lower() in text.lower():
                    return True
            elif self.search_mode == self.EXACT:
                if search_term == text:
                    return True
            elif self.search_mode == self.STARTS_WITH:
                if text.lower().startswith(search_term.lower()):
                    return True
            elif self.search_mode == self.ENDS_WITH:
                if text.lower().endswith(search_term.lower()):
                    return True
            elif self.search_mode == self.REGEX:
                try:
                    regex = QRegularExpression(search_term)
                    if regex.match(text).hasMatch():
                        return True
                except:
                    # If regex is invalid, fall back to contains
                    if search_term.lower() in text.lower():
                        return True
                    
        return False


class SchemaHelper:
    """Helper class for working with JSON schema"""

    @staticmethod
    def get_all_properties(schema, prefix=""):
        """Get all properties from a schema including nested ones"""
        properties = []

        if not schema or not isinstance(schema, dict):
            return properties

        schema_properties = schema.get("properties", {})

        for prop_name, prop_data in schema_properties.items():
            # Skip opendb_id for display
            if prop_name == "opendb_id":
                continue

            # Add the property itself
            prop_path = f"{prefix}{prop_name}" if prefix else prop_name
            properties.append(prop_path)

            # Check if this is an object with nested properties
            prop_type = prop_data.get("type")

            # Handle type that could be a list like ["object", "null"]
            if isinstance(prop_type, list):
                prop_type = next((t for t in prop_type if t != "null"), None)

            if prop_type == "object" and "properties" in prop_data:
                # Add nested properties with dot notation
                nested_prefix = f"{prop_path}."
                nested_props = SchemaHelper.get_all_properties(prop_data, nested_prefix)
                properties.extend(nested_props)

        return properties

    @staticmethod
    def get_required_fields(schema, prefix=""):
        """Get all required fields including nested ones with dot notation"""
        required = []

        if not schema or not isinstance(schema, dict):
            return required

        # Get top-level required fields
        for field in schema.get("required", []):
            if field != "opendb_id":  # Skip ID field
                field_path = f"{prefix}{field}" if prefix else field
                required.append(field_path)

        # Check for required fields in nested objects
        for prop_name, prop_data in schema.get("properties", {}).items():
            prop_type = prop_data.get("type")

            # Handle type that could be a list like ["object", "null"]
            if isinstance(prop_type, list):
                prop_type = next((t for t in prop_type if t != "null"), None)

            if prop_type == "object" and "properties" in prop_data:
                # Add nested required fields with dot notation
                nested_prefix = f"{prefix}{prop_name}." if prefix else f"{prop_name}."
                nested_required = SchemaHelper.get_required_fields(prop_data, nested_prefix)
                required.extend(nested_required)

        return required

    @staticmethod
    def validate_entry(entry_data, schema):
        """Validate a single entry against the schema, handling nested structures"""
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(entry_data), key=lambda e: e.path)

        results = {
            "is_valid": len(errors) == 0,
            "errors": [],
            "missing_required": [],
            "missing_optional": [],
            "type_mismatches": [],
        }

        # Get all properties and required fields, including nested ones
        all_fields = SchemaHelper.get_all_properties(schema)
        required_fields = SchemaHelper.get_required_fields(schema)
        optional_fields = [f for f in all_fields if f not in required_fields]

        # Check for each error from the validator
        for error in errors:
            results["errors"].append(str(error))

            # Handle missing required properties
            if error.validator == "required":
                parent_path = [str(p) for p in error.path]
                parent_prefix = ".".join(parent_path)
                parent_prefix = f"{parent_prefix}." if parent_prefix else ""

                for missing in error.validator_value:
                    # Skip opendb_id
                    if missing == "opendb_id":
                        continue

                    # Create the full path to the missing field
                    missing_path = f"{parent_prefix}{missing}"

                    # Check if this is a required field
                    if missing_path in required_fields:
                        results["missing_required"].append(missing_path)
                    else:
                        results["missing_optional"].append(missing_path)

            # Handle type mismatches
            elif error.validator == "type":
                path = ".".join(str(p) for p in error.path)
                expected = error.validator_value
                actual = type(error.instance).__name__
                results["type_mismatches"].append({
                    "field": path,
                    "expected": expected,
                    "actual": actual,
                    "value": error.instance,
                })

        # Check for empty values in required fields
        for field in required_fields:
            # Get the field value using dot notation
            parts = field.split(".")
            value = entry_data
            valid_path = True

            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    valid_path = False
                    break

            if valid_path:
                # Check for empty strings or null values
                if isinstance(value, str) and value.strip() == "":
                    if field not in results["missing_required"]:
                        results["missing_required"].append(field)
                elif value is None:
                    if field not in results["missing_required"]:
                        results["missing_required"].append(field)

        # Check for missing optional fields
        for field in optional_fields:
            # Get the field value using dot notation
            parts = field.split(".")
            value = entry_data
            valid_path = True

            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    valid_path = False
                    break

            if not valid_path or value is None:
                results["missing_optional"].append(field)
            elif isinstance(value, str) and value.strip() == "":
                results["missing_optional"].append(field)

        # Update is_valid based on our findings
        if results["missing_required"] or results["type_mismatches"]:
            results["is_valid"] = False

        return results

class JsonSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for JSON in a QTextEdit"""

    def __init__(self, parent=None, dark_theme=False):
        super().__init__(parent)

        self.dark_theme = dark_theme
        self.create_formats()

    def create_formats(self):
        # Create formatting rules
        self.formats = {}

        # Keywords (true, false, null)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(
            QColor("#CC7832") if self.dark_theme else QColor("#0000FF")
        )
        keyword_format.setFontWeight(QFont.Bold)
        self.formats["keyword"] = keyword_format

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(
            QColor("#6897BB") if self.dark_theme else QColor("#0000FF")
        )
        self.formats["number"] = number_format

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(
            QColor("#6A8759") if self.dark_theme else QColor("#008000")
        )
        self.formats["string"] = string_format

        # Properties
        property_format = QTextCharFormat()
        property_format.setForeground(
            QColor("#9876AA") if self.dark_theme else QColor("#FF00FF")
        )
        self.formats["property"] = property_format

        # Braces, brackets, commas, colons
        operator_format = QTextCharFormat()
        operator_format.setForeground(
            QColor("#A9B7C6") if self.dark_theme else QColor("#000000")
        )
        operator_format.setFontWeight(QFont.Bold)
        self.formats["operator"] = operator_format

    def update_theme(self, dark_theme):
        """Update the highlighter's color theme"""
        self.dark_theme = dark_theme
        self.create_formats()
        self.rehighlight()  # Reapply highlighting with new colors

    def highlightBlock(self, text):
        """Process the given text block for syntax highlighting"""
        # Match patterns
        patterns = {
            "keyword": r"\b(true|false|null)\b",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'"([^"\\]|\\.)*"',
            "property": r'"([^"\\]|\\.)*"(?=\s*:)',
            "operator": r"[\[\]{}:,]",
        }

        # Apply formatting for each pattern
        for pattern_type, pattern in patterns.items():
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.formats[pattern_type])
                index = expression.indexIn(text, index + length)


class EnhancedDataEditor(ThemedDialog):
    """
    Enhanced dialog for creating/editing hardware component data with nested properties support
    """

    def __init__(self, schema, data=None, parent=None):
        super().__init__(parent)
        self.schema = schema
        self.data = data or {}
        self.input_widgets = {}  # Will store all widgets with their paths
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Edit Component")
        self.resize(600, 700)

        main_layout = QVBoxLayout()
        
        # Create a scroll area to handle many fields
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Get schema properties and required fields
        properties = self.schema.get("properties", {})
        required_fields = SchemaHelper.get_required_fields(self.schema)
        
        # Create form fields recursively for all properties, including nested ones
        self.create_form_fields(form_layout, properties, required_fields, "")
        
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

        # Add buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_form_fields(self, form_layout, properties, required_fields, path_prefix=""):
        """Create form fields for properties recursively, handling nested objects"""
        for field_name, field_schema in properties.items():
            if field_name == "opendb_id":
                # Don't show the ID in the form
                continue

            # Create full path for this field
            full_path = f"{path_prefix}{field_name}" if path_prefix else field_name
            
            # Get field type, handling nullable types
            field_type = field_schema.get("type")
            if isinstance(field_type, list):
                # Handle nullable types like ["string", "null"]
                field_type = next((t for t in field_type if t != "null"), "string")
            
            # If this is an object with properties, create a group box for nested fields
            if field_type == "object" and "properties" in field_schema:
                # Create a group box for this object
                group_title = field_name.replace("_", " ").title()
                group_box = QGroupBox(group_title)
                nested_layout = QFormLayout()
                
                # Get nested properties and required fields
                nested_properties = field_schema.get("properties", {})
                nested_required = [f.replace(f"{full_path}.", "") for f in required_fields 
                                  if f.startswith(f"{full_path}.")]
                
                # Create nested form fields recursively
                self.create_form_fields(
                    nested_layout, 
                    nested_properties, 
                    nested_required, 
                    f"{full_path}."
                )
                
                group_box.setLayout(nested_layout)
                form_layout.addRow("", group_box)
                
            else:
                # Regular field, create appropriate widget
                
                # Create label with * for required fields
                label_text = field_name.replace("_", " ").title()
                if full_path in required_fields:
                    label_text += " *"
                
                # Get current value from data
                current_value = self.get_nested_value(self.data, full_path)
                
                # Create appropriate input widget based on field type
                widget = self.create_widget_for_type(field_type, field_schema, current_value)
                
                # Store the widget with its path for later retrieval
                self.input_widgets[full_path] = {
                    "widget": widget,
                    "type": field_type,
                    "schema": field_schema
                }
                
                form_layout.addRow(label_text, widget)

    def create_widget_for_type(self, field_type, field_schema, current_value):
        """Create appropriate widget based on field type"""
        if field_type == "string":
            if "enum" in field_schema:
                widget = ChangeTrackingComboBox(current_value)
                widget.addItems(field_schema["enum"])
                if current_value in field_schema["enum"]:
                    widget.setCurrentText(current_value)
            else:
                widget = ChangeTrackingLineEdit(current_value)
                
        elif field_type == "integer":
            # For integers, use the change tracking big number spin box with decimals=0
            widget = ChangeTrackingBigNumberSpinBox(current_value)
            widget.setDecimals(0)  # Force integer display
            
            # Set range from schema if specified
            if "minimum" in field_schema:
                widget.setMinimum(field_schema["minimum"])
            if "maximum" in field_schema:
                widget.setMaximum(field_schema["maximum"])
            
        elif field_type == "number":
            # For numbers, use the change tracking big number spin box
            widget = ChangeTrackingBigNumberSpinBox(current_value)
            widget.setDecimals(10)  # Support high precision
            
            # Set range from schema if specified
            if "minimum" in field_schema:
                widget.setMinimum(field_schema["minimum"])
            if "maximum" in field_schema:
                widget.setMaximum(field_schema["maximum"])
            
        elif field_type == "boolean":
            widget = ChangeTrackingCheckBox(current_value)
            
        elif field_type == "array":
            # Get the item type from the schema
            item_type = "string"  # Default type
            if "items" in field_schema and "type" in field_schema["items"]:
                items_type = field_schema["items"]["type"]
                # Handle cases where the type could be a list like ["string", "null"]
                if isinstance(items_type, list):
                    # Filter out "null" to get the main type
                    non_null_types = [t for t in items_type if t != "null"]
                    if non_null_types:
                        item_type = non_null_types[0]
                else:
                    item_type = items_type
                    
            # Create the custom change tracking array editor button
            widget = ChangeTrackingArrayButton(current_value, item_type)
            
        else:
            # Default to text input for unsupported types
            widget = ChangeTrackingLineEdit(current_value)
            
        return widget

    def get_nested_value(self, data, path):
        """Get a value from nested data structure using dot notation path"""
        if not path or not data:
            return None
            
        if "." not in path:
            return data.get(path)
            
        parts = path.split(".")
        current = data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
                
        return current

    def set_nested_value(self, data, path, value):
        """Set a value in nested data structure using dot notation path"""
        if not path:
            return
            
        if "." not in path:
            data[path] = value
            return
            
        parts = path.split(".")
        current = data
        
        # Navigate to the correct nesting level, creating dicts as needed
        for i, part in enumerate(parts[:-1]):  # All parts except the last
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                current[part] = {}
                
            current = current[part]
            
        # Set the value at the last level
        current[parts[-1]] = value

    def get_edited_data(self):
        """Get the data from form fields, handling nested structures"""
        result = self.data.copy()

        # Ensure we have an ID
        if "opendb_id" not in result or not result["opendb_id"]:
            result["opendb_id"] = str(uuid.uuid4())

        # Process all widgets and update the data
        for path, widget_info in self.input_widgets.items():
            widget = widget_info["widget"]
            field_type = widget_info["type"]
            
            # Get value from widget based on its type
            value = None
            
            if isinstance(widget, ChangeTrackingLineEdit):
                value = widget.text()
                    
            elif isinstance(widget, (ChangeTrackingSpinBox, ChangeTrackingSmartNumberSpinBox, ChangeTrackingBigNumberSpinBox)):
                value = widget.value()
                
            elif isinstance(widget, ChangeTrackingCheckBox):
                value = widget.isChecked()
                
            elif isinstance(widget, ChangeTrackingComboBox):
                value = widget.currentText()
                
            elif isinstance(widget, ChangeTrackingArrayButton):
                value = widget.get_array_data()
            
            # Update the data structure with this value
            self.set_nested_value(result, path, value)
            
        return result

class PropertyEditorWidget(QWidget):
    """Widget for editing a single property in a schema"""

    def __init__(self, property_name="", property_data=None, parent=None):
        super().__init__(parent)
        self.property_name = property_name
        self.property_data = property_data or {"type": "string"}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Property name
        name_layout = QHBoxLayout()
        name_label = QLabel("Property Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.property_name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Property type
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(
            ["string", "integer", "number", "boolean", "array", "object"]
        )
        self.type_combo.setCurrentText(self.property_data.get("type", "string"))
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # Type-specific options
        self.type_options_group = QGroupBox("Type Options")
        self.type_options_layout = QVBoxLayout()
        self.type_options_group.setLayout(self.type_options_layout)
        layout.addWidget(self.type_options_group)

        # Update type-specific options
        self.update_typeupdate_type_options()

        # Description
        description_layout = QHBoxLayout()
        description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        self.description_edit.setText(self.property_data.get("description", ""))
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)
        layout.addLayout(description_layout)

        # Required checkbox
        self.required_check = QCheckBox("Required")
        self.required_check.setChecked(False)  # This is managed by the parent dialog
        layout.addWidget(self.required_check)

        self.setLayout(layout)

    def on_type_changed(self, type_name):
        """Handle property type change"""
        self.property_data["type"] = type_name
        self.update_type_options()

    def update_type_options(self):
        """Update type-specific options based on current type"""
        # Clear existing options
        for i in reversed(range(self.type_options_layout.count())):
            item = self.type_options_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.type_options_layout.removeItem(item)

        type_name = self.type_combo.currentText()

        if type_name == "string":
            # String options: format, enum, pattern, etc.
            format_layout = QHBoxLayout()
            format_label = QLabel("Format:")
            self.format_combo = QComboBox()
            self.format_combo.addItems(
                ["", "date-time", "date", "time", "email", "uuid", "uri", "hostname"]
            )
            self.format_combo.setCurrentText(self.property_data.get("format", ""))
            format_layout.addWidget(format_label)
            format_layout.addWidget(self.format_combo)
            self.type_options_layout.addLayout(format_layout)

            # Enum values
            enum_label = QLabel("Enum Values (comma-separated):")
            self.enum_edit = QLineEdit()
            if "enum" in self.property_data:
                self.enum_edit.setText(", ".join(self.property_data["enum"]))
            self.type_options_layout.addWidget(enum_label)
            self.type_options_layout.addWidget(self.enum_edit)

        elif type_name in ["integer", "number"]:
            # Numeric options: minimum, maximum, etc.
            min_layout = QHBoxLayout()
            min_label = QLabel("Minimum:")
            
            # Always use BigNumberSpinBox for both integer and number
            self.min_spin = BigNumberSpinBox()
            
            # For integers, set decimals to 0
            if type_name == "integer":
                self.min_spin.setDecimals(0)
                
            if "minimum" in self.property_data:
                self.min_spin.setValue(self.property_data["minimum"])
            min_layout.addWidget(min_label)
            min_layout.addWidget(self.min_spin)
            self.type_options_layout.addLayout(min_layout)

            max_layout = QHBoxLayout()
            max_label = QLabel("Maximum:")
            
            # Always use BigNumberSpinBox for both integer and number
            self.max_spin = BigNumberSpinBox()
            
            # For integers, set decimals to 0
            if type_name == "integer":
                self.max_spin.setDecimals(0)
                
            if "maximum" in self.property_data:
                self.max_spin.setValue(self.property_data["maximum"])
            max_layout.addWidget(max_label)
            max_layout.addWidget(self.max_spin)
            self.type_options_layout.addLayout(max_layout)

        elif type_name == "boolean":
            # Boolean options: default value
            default_layout = QHBoxLayout()
            default_label = QLabel("Default:")
            self.default_check = QCheckBox()
            self.default_check.setChecked(self.property_data.get("default", False))
            default_layout.addWidget(default_label)
            default_layout.addWidget(self.default_check)
            self.type_options_layout.addLayout(default_layout)

        elif type_name == "array":
            # Array options: items type
            items_layout = QHBoxLayout()
            items_label = QLabel("Items Type:")
            self.items_combo = QComboBox()
            self.items_combo.addItems(
                ["string", "integer", "number", "boolean", "object"]
            )

            # Handle items type that could be a list like ["string", "null"]
            if "items" in self.property_data:
                items_type = self.property_data["items"].get("type", "string")
                if isinstance(items_type, list):
                    # Filter out "null" to get the main type
                    non_null_types = [t for t in items_type if t != "null"]
                    if non_null_types:
                        self.items_combo.setCurrentText(non_null_types[0])
                    else:
                        self.items_combo.setCurrentText("string")
                else:
                    self.items_combo.setCurrentText(items_type)

            items_layout.addWidget(items_label)
            items_layout.addWidget(self.items_combo)
            self.type_options_layout.addLayout(items_layout)

            # Nullable items checkbox
            self.items_nullable_check = QCheckBox("Allow null items in array")

            # Check if items type includes null
            if "items" in self.property_data:
                items_type = self.property_data["items"].get("type", "string")
                self.items_nullable_check.setChecked(
                    isinstance(items_type, list) and "null" in items_type
                )

            self.type_options_layout.addWidget(self.items_nullable_check)

        elif type_name == "object":
            # Object options
            info_label = QLabel("Use 'Advanced Configuration' for nested properties")
            self.type_options_layout.addWidget(info_label)

    def get_property_data(self):
        """Get the property data from form fields"""
        property_name = self.name_edit.text().strip()
        if not property_name:
            return None, None

        # Basic property data
        property_data = {"type": self.type_combo.currentText()}

        # Add description if provided
        description = self.description_edit.text().strip()
        if description:
            property_data["description"] = description

        # Type-specific options
        type_name = self.type_combo.currentText()

        if type_name == "string":
            # String options
            format_value = self.format_combo.currentText()
            if format_value:
                property_data["format"] = format_value

            # Enum values
            enum_text = self.enum_edit.text().strip()
            if enum_text:
                enum_values = [v.strip() for v in enum_text.split(",")]
                if enum_values:
                    property_data["enum"] = enum_values

        elif type_name in ["integer", "number"]:
            # Numeric options
            if hasattr(self, "min_spin") and self.min_spin.value() != 0:
                property_data["minimum"] = self.min_spin.value()

            if hasattr(self, "max_spin") and self.max_spin.value() != 0:
                property_data["maximum"] = self.max_spin.value()

        elif type_name == "boolean":
            # Boolean options
            if hasattr(self, "default_check"):
                property_data["default"] = self.default_check.isChecked()

        elif type_name == "array":
            # Array options
            if hasattr(self, "items_combo"):
                property_data["items"] = {"type": self.items_combo.currentText()}

        return property_name, property_data, self.required_check.isChecked()


class SchemaEditor(ThemedDialog):
    """
    Dialog for creating/editing JSON schemas
    """

    def __init__(self, schema_name=None, schema_data=None, parent=None):
        super().__init__(parent)
        self.schema_name = schema_name
        self.schema_data = schema_data or self.create_default_schema()
        self.setup_ui()

    def create_default_schema(self):
        """Create a default schema template"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "",
            "type": "object",
            "required": ["opendb_id"],
            "properties": {
                "opendb_id": {"type": "string", "format": "uuid"},
                "name": {"type": "string"},
            },
        }

    def setup_ui(self):
        if self.schema_name:
            self.setWindowTitle(f"Edit Schema: {self.schema_name}")
        else:
            self.setWindowTitle("Create New Schema")

        self.resize(900, 800)

        main_layout = QVBoxLayout()

        # Schema name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Schema Name:")
        self.name_input = QLineEdit()
        if self.schema_name:
            self.name_input.setText(self.schema_name)
            self.name_input.setEnabled(
                False
            )  # Don't allow changing existing schema names

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Title input
        title_layout = QHBoxLayout()
        title_label = QLabel("Schema Title:")
        self.title_input = QLineEdit()
        self.title_input.setText(self.schema_data.get("title", ""))
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        main_layout.addLayout(title_layout)

        # Tab widget for GUI / JSON modes
        self.tab_widget = QTabWidget()
        self.gui_tab = QWidget()
        self.json_tab = QWidget()

        # Setup GUI editor tab
        self.setup_gui_editor()
        self.tab_widget.addTab(self.gui_tab, "GUI Editor")

        # Setup JSON editor tab
        self.setup_json_editor()
        self.tab_widget.addTab(self.json_tab, "JSON Editor")

        main_layout.addWidget(self.tab_widget)

        # Connect tab changed signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Schema")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_gui_editor(self):
        """Set up the GUI editor tab"""
        layout = QVBoxLayout()

        # Property list and buttons
        list_layout = QHBoxLayout()

        # Property list
        self.property_list = QListWidget()
        self.property_list.setSelectionMode(QListWidget.SingleSelection)
        self.property_list.itemSelectionChanged.connect(self.on_property_selected)

        # Add existing properties
        properties = self.schema_data.get("properties", {})
        required_fields = self.schema_data.get("required", [])
        for prop_name, prop_data in properties.items():
            item = QListWidgetItem(prop_name)
            item.setData(
                Qt.UserRole,
                {
                    "name": prop_name,
                    "data": prop_data,
                    "required": prop_name in required_fields,
                },
            )
            self.property_list.addItem(item)

        list_layout.addWidget(self.property_list)

        # Property list buttons
        button_layout = QVBoxLayout()
        self.add_prop_button = QPushButton("Add Property")
        self.edit_prop_button = QPushButton("Edit Property")
        self.delete_prop_button = QPushButton("Delete Property")

        self.add_prop_button.clicked.connect(self.add_property)
        self.edit_prop_button.clicked.connect(self.edit_property)
        self.delete_prop_button.clicked.connect(self.delete_property)

        button_layout.addWidget(self.add_prop_button)
        button_layout.addWidget(self.edit_prop_button)
        button_layout.addWidget(self.delete_prop_button)
        button_layout.addStretch(1)  # Adds spacing

        list_layout.addLayout(button_layout)
        layout.addLayout(list_layout)

        # Property editor
        self.editor_group = QGroupBox("Property Editor")
        self.editor_layout = QVBoxLayout()
        self.property_editor = None
        self.editor_group.setLayout(self.editor_layout)
        layout.addWidget(self.editor_group)

        self.gui_tab.setLayout(layout)

    def setup_json_editor(self):
        """Set up the JSON editor tab"""
        layout = QVBoxLayout()

        # JSON editor with syntax highlighting
        self.json_editor = QTextEdit()
        self.json_editor.setAcceptRichText(False)
        self.json_editor.setLineWrapMode(QTextEdit.NoWrap)

        # Format the JSON nicely
        formatted_json = json.dumps(self.schema_data, indent=2)
        self.json_editor.setText(formatted_json)

        # Set a monospace font for the JSON editor
        font = QFont("Courier New", 10)
        self.json_editor.setFont(font)

        # Add syntax highlighter
        theme = (
            self.parent().settings.value("theme", "light") if self.parent() else "light"
        )
        self.highlighter = JsonSyntaxHighlighter(
            self.json_editor.document(), dark_theme=(theme == "dark")
        )

        layout.addWidget(self.json_editor)

        # Help text
        help_text = """
        <h3>Schema Format Help:</h3>
        <p>Use JSON Schema draft-07 format. Required fields:</p>
        <ul>
            <li>$schema - URL to schema spec (usually "http://json-schema.org/draft-07/schema#")</li>
            <li>title - The title of your component type</li>
            <li>type - Should be "object" for component data</li>
            <li>required - Array of required field names</li>
            <li>properties - Object containing field definitions</li>
        </ul>
        <p>Each property should have at minimum a "type" field specifying one of: string, integer, number, boolean, array, object</p>
        """
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.json_tab.setLayout(layout)

    def on_tab_changed(self, index):
        """Handle tab change events"""
        if index == 0:  # GUI Editor
            # Update GUI editor from JSON
            try:
                schema_data = json.loads(self.json_editor.toPlainText())
                self.update_gui_from_json(schema_data)
            except json.JSONDecodeError:
                QMessageBox.warning(
                    self,
                    "Invalid JSON",
                    "The JSON is invalid. Please fix the errors before switching tabs.",
                )
                self.tab_widget.setCurrentIndex(1)  # Switch back to JSON tab
        elif index == 1:  # JSON Editor
            # Update JSON from GUI editor
            schema_data = self.get_schema_from_gui()
            formatted_json = json.dumps(schema_data, indent=2)
            self.json_editor.setText(formatted_json)

    def update_gui_from_json(self, schema_data):
        """Update GUI editor from JSON schema data"""
        # Update schema data
        self.schema_data = schema_data

        # Update title
        self.title_input.setText(schema_data.get("title", ""))

        # Update property list
        self.property_list.clear()
        properties = schema_data.get("properties", {})
        required_fields = schema_data.get("required", [])

        for prop_name, prop_data in properties.items():
            item = QListWidgetItem(prop_name)
            item.setData(
                Qt.UserRole,
                {
                    "name": prop_name,
                    "data": prop_data,
                    "required": prop_name in required_fields,
                },
            )
            self.property_list.addItem(item)

    def get_schema_from_gui(self):
        """Get schema data from GUI editor"""
        # Basic schema data
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.title_input.text().strip(),
            "type": "object",
            "required": [],
            "properties": {},
        }

        # Add properties
        for i in range(self.property_list.count()):
            item = self.property_list.item(i)
            prop_data = item.data(Qt.UserRole)

            schema_data["properties"][prop_data["name"]] = prop_data["data"]

            if prop_data["required"]:
                schema_data["required"].append(prop_data["name"])

        return schema_data

    def on_property_selected(self):
        """Handle property selection in the list"""
        # Clear existing editor
        if self.property_editor:
            self.property_editor.deleteLater()
            self.property_editor = None

        # Get selected property
        selected_items = self.property_list.selectedItems()
        if not selected_items:
            return

        # Get property data
        item = selected_items[0]
        prop_data = item.data(Qt.UserRole)

        # Create property editor
        self.property_editor = PropertyEditorWidget(
            prop_data["name"], prop_data["data"]
        )
        self.property_editor.required_check.setChecked(prop_data["required"])

        # Add to layout
        self.editor_layout.addWidget(self.property_editor)

    def add_property(self):
        """Add a new property"""
        # Create property editor for new property
        if self.property_editor:
            self.property_editor.deleteLater()

        self.property_editor = PropertyEditorWidget()
        self.editor_layout.addWidget(self.property_editor)

        # Deselect any selected properties
        self.property_list.clearSelection()

    def edit_property(self):
        """Apply edits to the current property"""
        if not self.property_editor:
            return

        # Get property data from editor
        (
            property_name,
            property_data,
            is_required,
        ) = self.property_editor.get_property_data()

        if not property_name:
            QMessageBox.warning(
                self, "Invalid Property", "Property name cannot be empty."
            )
            return

        # Check if we're editing an existing property
        selected_items = self.property_list.selectedItems()
        if selected_items:
            # Update existing property
            item = selected_items[0]
            old_prop_data = item.data(Qt.UserRole)

            # Handle property name change
            if old_prop_data["name"] != property_name:
                # Check if property name already exists
                for i in range(self.property_list.count()):
                    other_item = self.property_list.item(i)
                    if (
                            other_item != item
                            and other_item.data(Qt.UserRole)["name"] == property_name
                    ):
                        QMessageBox.warning(
                            self,
                            "Duplicate Property",
                            f"Property '{property_name}' already exists.",
                        )
                        return

            # Update item
            item.setText(property_name)
            item.setData(
                Qt.UserRole,
                {"name": property_name, "data": property_data, "required": is_required},
            )
        else:
            # Add new property
            # Check if property name already exists
            for i in range(self.property_list.count()):
                item = self.property_list.item(i)
                if item.data(Qt.UserRole)["name"] == property_name:
                    QMessageBox.warning(
                        self,
                        "Duplicate Property",
                        f"Property '{property_name}' already exists.",
                    )
                    return

            # Add new item
            item = QListWidgetItem(property_name)
            item.setData(
                Qt.UserRole,
                {"name": property_name, "data": property_data, "required": is_required},
            )
            self.property_list.addItem(item)

        # Clear editor
        self.property_editor.deleteLater()
        self.property_editor = None

    def delete_property(self):
        """Delete the selected property"""
        selected_items = self.property_list.selectedItems()
        if not selected_items:
            return

        # Get property data
        item = selected_items[0]
        prop_data = item.data(Qt.UserRole)

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete property '{prop_data['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        # Delete item
        self.property_list.takeItem(self.property_list.row(item))

        # Clear editor
        if self.property_editor:
            self.property_editor.deleteLater()
            self.property_editor = None

    def validate_and_accept(self):
        """Validate schema before accepting"""
        try:
            # Get schema data from current tab
            if self.tab_widget.currentIndex() == 0:  # GUI Editor
                schema_data = self.get_schema_from_gui()
            else:  # JSON Editor
                schema_json = self.json_editor.toPlainText()
                schema_data = json.loads(schema_json)

            # Check schema name
            schema_name = self.name_input.text().strip()
            if not schema_name:
                QMessageBox.warning(self, "Missing Name", "Please enter a schema name.")
                return

            # Validate basic schema structure
            if not isinstance(schema_data, dict):
                QMessageBox.warning(
                    self, "Invalid Schema", "Schema must be a JSON object."
                )
                return

            # Check for required fields
            required_fields = ["$schema", "title", "type", "properties"]
            missing_fields = [f for f in required_fields if f not in schema_data]

            if missing_fields:
                QMessageBox.warning(
                    self,
                    "Invalid Schema",
                    f"Schema is missing required fields: {', '.join(missing_fields)}",
                )
                return

            if schema_data.get("type") != "object":
                QMessageBox.warning(
                    self,
                    "Invalid Schema",
                    "Schema type must be 'object' for component data.",
                )
                return

            if not isinstance(schema_data.get("properties"), dict):
                QMessageBox.warning(
                    self, "Invalid Schema", "Properties must be a JSON object."
                )
                return

            # Check if there are any properties
            if not schema_data.get("properties"):
                QMessageBox.warning(
                    self, "Invalid Schema", "Schema must have at least one property."
                )
                return

            # Store validated data and accept
            self.schema_name = schema_name
            self.schema_data = schema_data
            self.accept()

        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "Invalid JSON", f"JSON parsing error: {str(e)}")

    def get_schema_result(self):
        """Get the schema name and data"""
        return {"name": self.schema_name, "data": self.schema_data}


class SettingsDialog(ThemedDialog):
    """
    Dialog for application settings
    """

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Settings")
        self.resize(400, 300)

        layout = QVBoxLayout()

        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()

        self.light_radio = QRadioButton("Light Theme")
        self.dark_radio = QRadioButton("Dark Theme")

        # Set the current theme
        current_theme = self.settings.value("theme", "light")
        if current_theme == "dark":
            self.dark_radio.setChecked(True)
        else:
            self.light_radio.setChecked(True)

        theme_layout.addWidget(self.light_radio)
        theme_layout.addWidget(self.dark_radio)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Paths group
        paths_group = QGroupBox("File Paths")
        paths_layout = QFormLayout()

        # Schema directory
        self.schema_path = QLineEdit()
        self.schema_path.setText(str(SCHEMA_DIR))
        self.schema_path.setReadOnly(True)
        schema_browse = QPushButton("Browse...")
        schema_browse.clicked.connect(self.browse_schema_dir)

        schema_path_layout = QHBoxLayout()
        schema_path_layout.addWidget(self.schema_path)
        schema_path_layout.addWidget(schema_browse)

        # Data directory
        self.data_path = QLineEdit()
        self.data_path.setText(str(DATA_DIR))
        self.data_path.setReadOnly(True)
        data_browse = QPushButton("Browse...")
        data_browse.clicked.connect(self.browse_data_dir)

        data_path_layout = QHBoxLayout()
        data_path_layout.addWidget(self.data_path)
        data_path_layout.addWidget(data_browse)

        paths_layout.addRow("Schema Directory:", schema_path_layout)
        paths_layout.addRow("Data Directory:", data_path_layout)
        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)

        # Add buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_schema_dir(self):
        """Browse for schema directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Schema Directory", str(SCHEMA_DIR)
        )
        if dir_path:
            self.schema_path.setText(dir_path)

    def browse_data_dir(self):
        """Browse for data directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Data Directory", str(DATA_DIR)
        )
        if dir_path:
            self.data_path.setText(dir_path)

    def get_settings(self):
        """Get the settings values"""
        return {
            "theme": "dark" if self.dark_radio.isChecked() else "light",
            "schema_dir": self.schema_path.text(),
            "data_dir": self.data_path.text(),
        }

def apply_window_theme(window, dark_mode=False):
    """Apply dark/light theme to window title bar (Windows 10/11 only)"""
    if sys.platform == 'win32':
        try:
            from ctypes import windll, c_int, byref, sizeof
            
            # Windows 10 1809 or later
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            
            # Apply dark/light mode to title bar (1 = dark, 0 = light)
            windll.dwmapi.DwmSetWindowAttribute(
                int(window.winId()),
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                byref(c_int(1 if dark_mode else 0)),
                sizeof(c_int)
            )
        except Exception as e:
            print(f"Failed to set title bar theme: {e}")


class MainWindow(QMainWindow):
    """
    Main application window
    """

    def __init__(self):
        super().__init__()

        # Load settings
        self.settings = QSettings("OpenDB", "GUI")

        self.setWindowTitle("OpenDB GUI")
        self.resize(1200, 800)
        
        # Set application icon directly from scripts directory
        icon_path = str(SCRIPT_DIR / "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.current_category = None
        self.schemas = {}
        self.data = {}

        self.init_ui()
        self.apply_theme()
        self.load_schemas()

    def init_ui(self):
        # Create menu bar
        self.create_menu_bar()

        # Create toolbar
        self.create_toolbar()

        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top controls
        top_controls = QHBoxLayout()

        # Category selection
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)

        # Search controls
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name or ID...")
        self.search_box.textChanged.connect(self.on_search_changed)
        
        # Search mode dropdown
        self.search_mode_combo = QComboBox()
        self.search_mode_combo.addItem("Contains", AdvancedFilterProxyModel.CONTAINS)
        self.search_mode_combo.addItem("Exact Match", AdvancedFilterProxyModel.EXACT)
        self.search_mode_combo.addItem("Starts With", AdvancedFilterProxyModel.STARTS_WITH)
        self.search_mode_combo.addItem("Ends With", AdvancedFilterProxyModel.ENDS_WITH)
        self.search_mode_combo.addItem("Regex", AdvancedFilterProxyModel.REGEX)
        self.search_mode_combo.currentIndexChanged.connect(self.on_search_mode_changed)
        
        # Search column dropdown - will be populated when a category is selected
        self.search_column_combo = QComboBox()
        self.search_column_combo.addItem("All Columns")
        self.search_column_combo.currentIndexChanged.connect(self.on_search_column_changed)
        
        # Clear search button
        self.clear_search_button = QPushButton("Clear")
        self.clear_search_button.clicked.connect(self.clear_search)
        
        # Add all search controls to the layout
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_mode_combo)
        search_layout.addWidget(self.search_column_combo)
        search_layout.addWidget(self.clear_search_button)
        
        top_controls.addWidget(category_label)
        top_controls.addWidget(self.category_combo)
        top_controls.addLayout(search_layout)
        top_controls.addStretch(1)

        # Validation controls
        self.validation_button = QPushButton("Validate All")
        self.validation_button.clicked.connect(self.validate_all_entries)
        top_controls.addWidget(self.validation_button)

        main_layout.addLayout(top_controls)

        # Table view
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        self.table_view.doubleClicked.connect(self.on_row_double_clicked)
        self.table_view.setAlternatingRowColors(True)

        self.table_view.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        self.table_view.setVerticalScrollMode(QTableView.ScrollPerPixel)

        self.table_model = DataTableModel()
        self.proxy_model = AdvancedFilterProxyModel()
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setDynamicSortFilter(True)

        self.table_view.setModel(self.proxy_model)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        # Enable sorting and make headers clickable
        self.table_view.setSortingEnabled(True)
        # Set clickable property explicitly
        self.table_view.horizontalHeader().setSectionsClickable(True)
        # Configure the sorting
        self.proxy_model.sort(-1, Qt.AscendingOrder)  # Start with no sorting

        main_layout.addWidget(self.table_view)

        # Bottom controls
        bottom_controls = QHBoxLayout()

        self.add_button = QPushButton("Add New")
        self.add_button.clicked.connect(self.add_new_entry)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_selected_entry)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected_entry)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_data)

        bottom_controls.addWidget(self.add_button)
        bottom_controls.addWidget(self.edit_button)
        bottom_controls.addWidget(self.delete_button)
        bottom_controls.addWidget(self.refresh_button)
        bottom_controls.addStretch(1)

        main_layout.addLayout(bottom_controls)

        # Set up the central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Legend for validation colors
        legend_widget = QWidget()
        legend_layout = QHBoxLayout()
        legend_layout.setContentsMargins(10, 0, 10, 0)

        # Required missing
        red_box = QLabel()
        red_box.setFixedSize(16, 16)
        red_box.setStyleSheet("background-color: rgb(255, 200, 200);")
        legend_layout.addWidget(red_box)
        legend_layout.addWidget(QLabel("Missing Required"))

        # Type mismatch
        orange_box = QLabel()
        orange_box.setFixedSize(16, 16)
        orange_box.setStyleSheet("background-color: rgb(255, 230, 200);")
        legend_layout.addWidget(orange_box)
        legend_layout.addWidget(QLabel("Type Mismatch"))

        # Optional missing
        yellow_box = QLabel()
        yellow_box.setFixedSize(16, 16)
        yellow_box.setStyleSheet("background-color: rgb(255, 255, 200);")
        legend_layout.addWidget(yellow_box)
        legend_layout.addWidget(QLabel("Missing Optional"))

        legend_widget.setLayout(legend_layout)
        self.status_bar.addPermanentWidget(legend_widget)

    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Actions for File menu
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Schema menu
        schema_menu = menubar.addMenu("Schema")

        # Actions for Schema menu
        create_schema_action = QAction("Create New Schema", self)
        create_schema_action.triggered.connect(self.create_new_schema)

        edit_schema_action = QAction("Edit Current Schema", self)
        edit_schema_action.triggered.connect(self.edit_current_schema)

        schema_menu.addAction(create_schema_action)
        schema_menu.addAction(edit_schema_action)

        # Settings menu
        settings_menu = menubar.addMenu("Settings")

        # Actions for Settings menu
        app_settings_action = QAction("Application Settings", self)
        app_settings_action.triggered.connect(self.show_settings)

        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)

        settings_menu.addAction(app_settings_action)
        settings_menu.addAction(toggle_theme_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # Actions for Help menu
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add actions to toolbar
        # New entry
        new_entry_action = QAction("New Entry", self)
        new_entry_action.triggered.connect(self.add_new_entry)
        toolbar.addAction(new_entry_action)

        # Edit entry
        edit_entry_action = QAction("Edit Entry", self)
        edit_entry_action.triggered.connect(self.edit_selected_entry)
        toolbar.addAction(edit_entry_action)

        # Delete entry
        delete_entry_action = QAction("Delete Entry", self)
        delete_entry_action.triggered.connect(self.delete_selected_entry)
        toolbar.addAction(delete_entry_action)

        toolbar.addSeparator()

        # Validate all
        validate_action = QAction("Validate All", self)
        validate_action.triggered.connect(self.validate_all_entries)
        toolbar.addAction(validate_action)

        toolbar.addSeparator()

        # New schema
        new_schema_action = QAction("New Schema", self)
        new_schema_action.triggered.connect(self.create_new_schema)
        toolbar.addAction(new_schema_action)

        # Edit schema
        edit_schema_action = QAction("Edit Schema", self)
        edit_schema_action.triggered.connect(self.edit_current_schema)
        toolbar.addAction(edit_schema_action)

        toolbar.addSeparator()

        # Toggle theme
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_theme = self.settings.value("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"
        self.settings.setValue("theme", new_theme)
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme"""
        theme = self.settings.value("theme", "light")
        is_dark = theme == "dark"
        
        if is_dark:
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)
        
        # Apply theme to main window title bar
        apply_window_theme(self, dark_mode=is_dark)
        
        # Store current theme in class variable for dialogs to access
        self.is_dark_mode = is_dark

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the settings
            new_settings = dialog.get_settings()

            # Apply settings
            self.settings.setValue("theme", new_settings["theme"])
            self.settings.setValue("schema_dir", new_settings["schema_dir"])
            self.settings.setValue("data_dir", new_settings["data_dir"])

            # Apply theme
            self.apply_theme()

            # Update paths if needed
            schema_dir = Path(new_settings["schema_dir"])
            data_dir = Path(new_settings["data_dir"])

            if schema_dir != SCHEMA_DIR or data_dir != DATA_DIR:
                # We'd need to restart for path changes
                # For now just notify the user
                QMessageBox.information(
                    self,
                    "Path Changes",
                    "Path changes will take effect after restarting the application.",
                )

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Hardware DB GUI",
            """
                          <h1>Hardware DB GUI</h1>
                          <p>A graphical interface for managing hardware component data with JSON schemas.</p>
                          <p>Features:</p>
                          <ul>
                          <li>Create, edit, and delete hardware components</li>
                          <li>Manage JSON schemas</li>
                          <li>Validate data against schemas</li>
                          <li>Search and filter components</li>
                          <li>Light and dark themes</li>
                          </ul>
                          """,
        )

    def create_new_schema(self):
        """Create a new schema"""
        dialog = SchemaEditor(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the schema
            schema_result = dialog.get_schema_result()
            schema_name = schema_result["name"]
            schema_data = schema_result["data"]

            # Check if schema already exists
            schema_path = SCHEMA_DIR / f"{schema_name}.schema.json"
            if schema_path.exists():
                confirm = QMessageBox.question(
                    self,
                    "Schema Exists",
                    f"Schema '{schema_name}' already exists. Overwrite?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if confirm != QMessageBox.Yes:
                    return

            # Save the schema
            try:
                with open(schema_path, "w", encoding="utf-8") as f:
                    json.dump(schema_data, f, indent=2, ensure_ascii=False)

                # Reload schemas
                self.load_schemas()

                # Select the new schema
                index = self.category_combo.findText(schema_name)
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)

                QMessageBox.information(
                    self,
                    "Schema Created",
                    f"Schema '{schema_name}' has been created successfully.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Save Error", f"Failed to save schema: {str(e)}"
                )

    def edit_current_schema(self):
        """Edit the current schema"""
        if not self.current_category:
            QMessageBox.warning(
                self, "No Schema Selected", "Please select a schema to edit."
            )
            return

        # Get current schema
        schema_data = self.schemas.get(self.current_category, {})

        # Open editor
        dialog = SchemaEditor(self.current_category, schema_data, self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the schema
            schema_result = dialog.get_schema_result()
            schema_name = schema_result["name"]
            schema_data = schema_result["data"]

            # Save the schema
            schema_path = SCHEMA_DIR / f"{schema_name}.schema.json"
            try:
                with open(schema_path, "w", encoding="utf-8") as f:
                    json.dump(schema_data, f, indent=2, ensure_ascii=False)

                # Reload schemas
                self.schemas[schema_name] = schema_data

                # Reload data with the updated schema
                self.load_category_data(schema_name)

                QMessageBox.information(
                    self,
                    "Schema Updated",
                    f"Schema '{schema_name}' has been updated successfully.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Save Error", f"Failed to save schema: {str(e)}"
                )

    def load_schemas(self):
        """Load all available schemas"""
        schema_files = list(SCHEMA_DIR.glob("*.schema.json"))
        self.schemas = {}

        # Block signals during loading
        self.category_combo.blockSignals(True)
        self.category_combo.clear()

        for schema_file in schema_files:
            category = schema_file.name.split(".")[0]
            try:
                with open(schema_file, encoding="utf-8") as f:
                    schema = json.load(f)
                self.schemas[category] = schema
                self.category_combo.addItem(category)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Schema Error",
                    f"Failed to load schema {schema_file}: {str(e)}",
                )

        self.category_combo.blockSignals(False)

        # Load first category if available
        if self.category_combo.count() > 0:
            self.on_category_changed(0)

    def load_category_data(self, category):
        """Load all data for a specific category, with support for nested schemas"""
        self.current_category = category
        self.data = {}

        category_dir = DATA_DIR / category
        category_dir.mkdir(exist_ok=True)

        data_files = list(category_dir.glob("*.json"))
        entries = []

        for data_file in data_files:
            try:
                with open(data_file, encoding="utf-8") as f:
                    entry = json.load(f)

                    # Store by ID for faster lookup
                    entry_id = entry.get("opendb_id")
                    if entry_id:
                        self.data[entry_id] = entry
                        entries.append(entry)
            except Exception as e:
                QMessageBox.warning(
                    self, "Data Error", f"Failed to load data {data_file}: {str(e)}"
                )

        # Get schema
        schema = self.schemas.get(category, {})

        # Create headers from schema properties, including nested ones
        headers = ["opendb_id"]  # Always include ID
        schema_properties = SchemaHelper.get_all_properties(schema)
        headers.extend(schema_properties)

        # Update the table model
        self.table_model = DataTableModel(entries, headers)

        # Set required fields, including nested ones
        required_fields = SchemaHelper.get_required_fields(schema)
        self.table_model.set_required_fields(required_fields)

        # Set up the proxy model
        self.proxy_model.setSourceModel(self.table_model)
        
        # Update search columns dropdown
        self.update_search_columns()

        # Validate data
        self.validate_all_entries()

        # Update status
        self.status_bar.showMessage(
            f"Loaded {len(entries)} entries for category {category}"
        )

    def on_category_changed(self, index):
        """Handle category selection change"""
        if index >= 0:
            category = self.category_combo.itemText(index)
            self.load_category_data(category)

    def on_search_changed(self, text):
        """Handle search text change"""
        self.proxy_model.setFilterRegExp(text)
        # Update status bar with count of filtered items
        visible_count = self.proxy_model.rowCount()
        total_count = self.table_model.rowCount()
        self.status_bar.showMessage(f"Displaying {visible_count} of {total_count} entries")
        
    def on_search_mode_changed(self, index):
        """Handle search mode change"""
        mode = self.search_mode_combo.currentData()
        self.proxy_model.setSearchMode(mode)
        # Re-apply the current search text to trigger filtering with new mode
        self.on_search_changed(self.search_box.text())
        
    def on_search_column_changed(self, index):
        """Handle search column change"""
        if index == 0:  # "All Columns"
            self.proxy_model.setSearchColumns([])
        else:
            # Adjust for 0-based column index (the combo box first item is "All Columns")
            column_index = index - 1
            self.proxy_model.setSearchColumns([column_index])
            
        # Re-apply the current search text
        self.on_search_changed(self.search_box.text())
        
    def clear_search(self):
        """Clear the search box"""
        self.search_box.clear()
        self.search_mode_combo.setCurrentIndex(0)  # Reset to "Contains"
        self.search_column_combo.setCurrentIndex(0)  # Reset to "All Columns"
        
    def update_search_columns(self):
        """Update the search column dropdown with current table headers"""
        # Save current selection
        current_text = self.search_column_combo.currentText()
        
        # Clear and re-populate
        self.search_column_combo.clear()
        self.search_column_combo.addItem("All Columns")
        
        # Add all table headers
        for i in range(self.table_model.columnCount()):
            column_name = self.table_model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if column_name:
                self.search_column_combo.addItem(column_name)
                
        # Try to restore previous selection
        index = self.search_column_combo.findText(current_text)
        if index >= 0:
            self.search_column_combo.setCurrentIndex(index)
        else:
            self.search_column_combo.setCurrentIndex(0)  # Default to "All Columns"

    def validate_entry(self, entry_data, schema):
        """Validate a single entry against the schema, handling nested structures"""
        return SchemaHelper.validate_entry(entry_data, schema)

    def add_new_entry(self):
        """Add a new entry"""
        if not self.current_category:
            return

        schema = self.schemas.get(self.current_category, {})

        # Create a new entry with default values
        new_entry = {}
        new_entry["opendb_id"] = str(uuid.uuid4())

        # Open editor dialog
        dialog = EnhancedDataEditor(schema, new_entry, self)
        if dialog.exec_() == QDialog.Accepted:
            # Get edited data
            edited_data = dialog.get_edited_data()

            # Save to file
            self.save_entry(edited_data)

            # Refresh data
            self.refresh_data()

    def edit_selected_entry(self):
        """Edit the selected entry"""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, "No Selection", "Please select an entry to edit.")
            return

        # Get the first selected row
        proxy_index = selected_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_row = source_index.row()

        # Get data for the selected row
        entry_data = self.table_model.get_row_data(source_row)
        if not entry_data:
            return

        # Open editor dialog
        schema = self.schemas.get(self.current_category, {})
        dialog = EnhancedDataEditor(schema, entry_data, self)
        if dialog.exec_() == QDialog.Accepted:
            # Get edited data
            edited_data = dialog.get_edited_data()

            # Save to file
            self.save_entry(edited_data)

            # Refresh data
            self.refresh_data()

    def validate_all_entries(self):
        """Validate all entries for the current category"""
        if not self.current_category:
            return

        schema = self.schemas.get(self.current_category, {})
        validation_results = {}
        valid_count = 0
        total_count = len(self.data)

        for entry_id, entry_data in self.data.items():
            results = self.validate_entry(entry_data, schema)
            validation_results[entry_id] = results

            if results["is_valid"]:
                valid_count += 1

        # Update the table model with validation results
        self.table_model.set_validation_results(validation_results)

        # Update status
        self.status_bar.showMessage(
            f"Validation: {valid_count}/{total_count} entries are valid"
        )

    def delete_selected_entry(self):
        """Delete the selected entry"""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(
                self, "No Selection", "Please select an entry to delete."
            )
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete the selected entry?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        # Get the first selected row
        proxy_index = selected_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_row = source_index.row()

        # Get data for the selected row
        entry_data = self.table_model.get_row_data(source_row)
        if not entry_data:
            return

        # Get the ID
        entry_id = entry_data.get("opendb_id")
        if not entry_id:
            return

        # Delete the file
        file_path = DATA_DIR / self.current_category / f"{entry_id}.json"
        try:
            if file_path.exists():
                file_path.unlink()

            # Remove from data
            if entry_id in self.data:
                del self.data[entry_id]

            # Refresh data
            self.refresh_data()
        except Exception as e:
            QMessageBox.critical(self, "Deletion Error", f"Failed to delete file: {str(e)}")

    def save_entry(self, entry_data):
        """Save an entry to file"""
        entry_id = entry_data.get("opendb_id")
        if not entry_id:
            return

        file_path = DATA_DIR / self.current_category / f"{entry_id}.json"

        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(exist_ok=True)

            # Write to file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(entry_data, f, indent=2, ensure_ascii=False)

            # Update in-memory data
            self.data[entry_id] = entry_data

            # Show success message
            self.status_bar.showMessage(f"Saved entry {entry_id}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save file: {str(e)}")

    def refresh_data(self):
        """Refresh data for the current category"""
        if self.current_category:
            self.load_category_data(self.current_category)

    def on_row_double_clicked(self, index):
        """Handle double-click on table row"""
        self.edit_selected_entry()

    def show_context_menu(self, position):
        """Show context menu for table row"""
        # Get selected indexes
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            return

        # Create menu
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        validate_action = menu.addAction("Validate")

        # Show menu and handle actions
        action = menu.exec_(self.table_view.viewport().mapToGlobal(position))

        if action == edit_action:
            self.edit_selected_entry()
        elif action == delete_action:
            self.delete_selected_entry()
        elif action == validate_action:
            # Validate just this entry
            proxy_index = selected_indexes[0]
            source_index = self.proxy_model.mapToSource(proxy_index)
            source_row = source_index.row()

            # Get data for the selected row
            entry_data = self.table_model.get_row_data(source_row)
            if entry_data:
                schema = self.schemas.get(self.current_category, {})
                results = self.validate_entry(entry_data, schema)

                # Show detailed validation results
                self.show_validation_results(entry_data.get("name", "Entry"), results)

    def show_validation_results(self, entry_name, results):
        """Show detailed validation results for an entry"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Validation Results: {entry_name}")
        dialog.resize(600, 400)

        layout = QVBoxLayout()

        # Summary label
        summary_label = QLabel()
        if results["is_valid"]:
            summary_label.setText("✅ Entry is valid")
            summary_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            summary_label.setText("❌ Entry has validation issues")
            summary_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(summary_label)

        # Details group box
        details_group = QGroupBox("Details")
        details_layout = QVBoxLayout()

        # Missing required fields
        if results["missing_required"]:
            req_label = QLabel("Missing Required Fields:")
            req_label.setStyleSheet("color: red; font-weight: bold;")
            details_layout.addWidget(req_label)

            for field in results["missing_required"]:
                details_layout.addWidget(QLabel(f"• {field}"))

            details_layout.addWidget(QLabel(""))  # Spacer

        # Type mismatches
        if results["type_mismatches"]:
            type_label = QLabel("Type Mismatches:")
            type_label.setStyleSheet("color: orange; font-weight: bold;")
            details_layout.addWidget(type_label)

            for mismatch in results["type_mismatches"]:
                mismatch_text = f"• {mismatch['field']}: expected {mismatch['expected']}, got {mismatch['actual']}"
                details_layout.addWidget(QLabel(mismatch_text))

            details_layout.addWidget(QLabel(""))  # Spacer

        # Missing optional fields
        if results["missing_optional"]:
            opt_label = QLabel("Missing Optional Fields:")
            opt_label.setStyleSheet("color: #B0B000; font-weight: bold;")
            details_layout.addWidget(opt_label)

            for field in results["missing_optional"]:
                details_layout.addWidget(QLabel(f"• {field}"))

        # Raw errors
        if results["errors"] and not (
                results["missing_required"] or results["type_mismatches"]
        ):
            err_label = QLabel("Other Validation Errors:")
            err_label.setStyleSheet("color: red;")
            details_layout.addWidget(err_label)

            for error in results["errors"]:
                details_layout.addWidget(QLabel(f"• {error}"))

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication([])
    
    # Set application icon for all windows directly from scripts directory
    icon_path = str(Path(__file__).parent / "favicon.png")
    app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())