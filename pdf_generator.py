from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import pandas as pd

def register_fonts():
    """Registers Arial font for Unicode support."""
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
        return 'Arial', 'Arial-Bold'
    except Exception as e:
        # Fallback to Helvetica if Arial is not found
        return 'Helvetica', 'Helvetica-Bold'

def create_styled_table(data, col_widths, font_normal, font_bold, header_bg='#667eea', row_bg=colors.beige):
    """Creates a ReportLab Table with standard styling."""
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), row_bg),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), font_normal),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    return t

def fig_to_image(fig, width=6*inch, height=4*inch):
    """Converts a Plotly figure to a ReportLab Image."""
    if fig is None:
        return None
    try:
        # Convert to PNG bytes
        img_bytes = fig.to_image(format="png", width=800, height=500, scale=2)
        return Image(BytesIO(img_bytes), width=width, height=height)
    except Exception as e:
        print(f"Error converting figure to image: {e}")
        return None

def generate_expense_report(df, options, charts=None):
    """
    Generates the PDF report and returns the bytes.
    
    Args:
        df (pd.DataFrame): The filtered dataframe containing expense data.
        options (dict): Configuration options for the report.
        charts (dict): Dictionary of Plotly figures to include.
    
    Returns:
        bytes: The generated PDF data.
    """
    buffer = BytesIO()
    if charts is None:
        charts = {}
    
    # Configure Page Size and Orientation
    page_size_map = {
        "A4": A4, "Letter": letter, "Legal": (8.5*inch, 14*inch),
        "A3": (11.7*inch, 16.5*inch), "A5": (5.8*inch, 8.3*inch)
    }
    selected_size = page_size_map.get(options.get('page_size', 'A4'), A4)
    
    if options.get('orientation') == 'Landscape':
        pagesize = landscape(selected_size)
        content_width = pagesize[0] - 60
    else:
        pagesize = portrait(selected_size)
        content_width = pagesize[0] - 60
        
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    
    elements = []
    font_normal, font_bold = register_fonts()
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_bold,
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=font_bold,
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12
    )
    cover_info_style = ParagraphStyle(
        'CoverInfo',
        parent=styles['Normal'],
        fontName=font_normal,
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    # Calculate Metrics
    total_cost = df['Cost'].sum()
    total_sessions = df['Session_ID'].nunique() if 'Session_ID' in df.columns else 0
    avg_cost = total_cost / total_sessions if total_sessions > 0 else 0
    
    # --- Content Generation ---
    
    # Cover Page
    if options.get('include_cover', True):
        elements.append(Paragraph("Expense Analysis Report", title_style))
        elements.append(Spacer(1, 50))
        
        elements.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", cover_info_style))
        elements.append(Paragraph(f"<b>Total Records:</b> {len(df)}", cover_info_style))
        elements.append(Spacer(1, 50))
        
        # Summary Box
        summary_data = [
            ['Key Metrics', 'Value'],
            ['Total Cost', f'Rs. {total_cost:,.2f}'],
            ['Total Sessions', f'{total_sessions}'],
            ['Average Cost/Session', f'Rs. {avg_cost:,.2f}']
        ]
        # Custom style for summary table (larger font)
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), font_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), font_normal),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
        ]))
        elements.append(summary_table)
        elements.append(PageBreak())
    else:
        elements.append(Paragraph("Expense Analysis Report", title_style))
        elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", cover_info_style))
        elements.append(Spacer(1, 20))

    # KPI Summary
    if options.get('include_kpi', True):
        elements.append(Paragraph("Key Performance Indicators", heading_style))
        kpi_data = [
            ['Metric', 'Value'],
            ['Total Cost', f'Rs. {total_cost:,.2f}'],
            ['Total Sessions', f'{total_sessions}'],
            ['Average Cost per Session', f'Rs. {avg_cost:,.2f}']
        ]
        elements.append(create_styled_table(kpi_data, [3*inch, 3*inch], font_normal, font_bold))
        elements.append(Spacer(1, 20))

    # Region Summary
    if options.get('include_region', True):
        elements.append(Paragraph("Regional Summary", heading_style))
        region_stats = df.groupby('Region').agg({
            'Cost': 'sum',
            'Session_ID': 'nunique',
            'Client Name': 'nunique'
        }).reset_index()
        region_stats = region_stats.sort_values('Cost', ascending=False)
        
        region_data = [['Region', 'Total Cost', 'Sessions', 'Clients']]
        for _, row in region_stats.iterrows():
            region_data.append([
                str(row['Region']),
                f"Rs. {row['Cost']:,.2f}",
                str(row['Session_ID']),
                str(row['Client Name'])
            ])
        elements.append(create_styled_table(region_data, [1.5*inch]*4, font_normal, font_bold))
        elements.append(Spacer(1, 20))
        
        # Region Charts
        if 'region_pie' in charts:
            elements.append(fig_to_image(charts['region_pie'], width=6*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'region_trend' in charts:
            elements.append(fig_to_image(charts['region_trend'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'region_bar_group' in charts:
            elements.append(fig_to_image(charts['region_bar_group'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 20))

    # Trainer Summary
    if options.get('include_trainer', True):
        elements.append(Paragraph("Trainer Summary", heading_style))
        trainer_stats = df.groupby('Name of Trainer').agg({
            'Cost': 'sum',
            'Session_ID': 'nunique'
        }).reset_index()
        trainer_stats['Avg Cost'] = trainer_stats['Cost'] / trainer_stats['Session_ID']
        trainer_stats = trainer_stats.sort_values('Cost', ascending=False).head(10)
        
        trainer_data = [['Trainer', 'Total Cost', 'Sessions', 'Avg Cost']]
        for _, row in trainer_stats.iterrows():
            trainer_data.append([
                str(row['Name of Trainer']),
                f"Rs. {row['Cost']:,.2f}",
                str(row['Session_ID']),
                f"Rs. {row['Avg Cost']:,.2f}"
            ])
        elements.append(create_styled_table(trainer_data, [1.5*inch]*4, font_normal, font_bold))
        elements.append(Spacer(1, 20))
        
        # Trainer Charts
        if 'trainer_pie' in charts:
            elements.append(fig_to_image(charts['trainer_pie'], width=6*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'trainer_efficiency' in charts:
            elements.append(fig_to_image(charts['trainer_efficiency'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'trainer_payment' in charts:
            elements.append(fig_to_image(charts['trainer_payment'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 20))

    # Client Summary
    if options.get('include_client', True):
        elements.append(Paragraph("Client Summary (Top 15)", heading_style))
        client_summary = df.groupby(['Region', 'Client Name']).agg({
            'Cost': 'sum',
            'Session_ID': 'nunique'
        }).reset_index()
        client_summary = client_summary.sort_values('Cost', ascending=False).head(15)
        
        client_data = [['Region', 'Client', 'Total Cost', 'Sessions']]
        for _, row in client_summary.iterrows():
            client_data.append([
                str(row['Region']),
                str(row['Client Name'])[:20],
                f"Rs. {row['Cost']:,.2f}",
                str(row['Session_ID'])
            ])
        elements.append(create_styled_table(client_data, [1.2*inch, 2*inch, 1.5*inch, 1.3*inch], font_normal, font_bold))
        elements.append(Spacer(1, 20))
        
        # Client Charts
        if 'client_cost' in charts:
            elements.append(fig_to_image(charts['client_cost'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'client_scatter' in charts:
            elements.append(fig_to_image(charts['client_scatter'], width=7*inch, height=4*inch))
            elements.append(Spacer(1, 20))

    # Payment Analysis
    if options.get('include_payment', True):
        elements.append(Paragraph("Payment Method Distribution", heading_style))
        payment_dist = df.groupby('Payment Type')['Cost'].sum().reset_index()
        payment_dist = payment_dist.sort_values('Cost', ascending=False)
        
        payment_data = [['Payment Type', 'Total Cost', 'Percentage']]
        for _, row in payment_dist.iterrows():
            percentage = (row['Cost'] / total_cost) * 100 if total_cost > 0 else 0
            payment_data.append([
                str(row['Payment Type']),
                f"Rs. {row['Cost']:,.2f}",
                f"{percentage:.1f}%"
            ])
        elements.append(create_styled_table(payment_data, [2*inch]*3, font_normal, font_bold))
        elements.append(Spacer(1, 20))
        
        # Payment Charts
        if 'payment_pie' in charts:
            elements.append(fig_to_image(charts['payment_pie'], width=6*inch, height=4*inch))
            elements.append(Spacer(1, 10))
        if 'payment_stack' in charts:
            elements.append(fig_to_image(charts['payment_stack'], width=7*inch, height=4*inch))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
