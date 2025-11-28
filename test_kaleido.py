"""
Test script to verify kaleido installation and chart conversion.
Run this to diagnose PDF chart generation issues.
"""

import plotly.express as px
import pandas as pd

print("=" * 60)
print("Testing Kaleido Installation and Chart Conversion")
print("=" * 60)

# Test 1: Check if kaleido is installed
print("\n1. Checking kaleido installation...")
try:
    import kaleido
    version = getattr(kaleido, '__version__', 'unknown')
    print(f"   ✓ Kaleido is installed (version: {version})")
except ImportError as e:
    print(f"   ✗ Kaleido is NOT installed: {e}")
    print("   Please run: pip install kaleido")
    exit(1)

# Test 2: Create a simple chart
print("\n2. Creating a simple test chart...")
try:
    df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 20, 15, 25]
    })
    fig = px.bar(df, x='Category', y='Value', title='Test Chart')
    print("   ✓ Chart created successfully")
except Exception as e:
    print(f"   ✗ Failed to create chart: {e}")
    exit(1)

# Test 3: Convert chart to image
print("\n3. Converting chart to PNG image...")
try:
    img_bytes = fig.to_image(format="png", width=800, height=500, scale=2)
    print(f"   ✓ Chart converted successfully")
    print(f"   Image size: {len(img_bytes)} bytes")
except Exception as e:
    print(f"   ✗ Failed to convert chart: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Save test image
print("\n4. Saving test image...")
try:
    with open("test_chart.png", "wb") as f:
        f.write(img_bytes)
    print("   ✓ Test image saved as 'test_chart.png'")
except Exception as e:
    print(f"   ✗ Failed to save image: {e}")
    exit(1)

print("\n" + "=" * 60)
print("All tests passed! Kaleido is working correctly.")
print("=" * 60)
print("\nIf charts are still not appearing in your PDF:")
print("1. Check the Streamlit console for error messages")
print("2. Verify that charts are being passed to the PDF generator")
print("3. Look for 'ERROR' messages in the PDF generation output")
