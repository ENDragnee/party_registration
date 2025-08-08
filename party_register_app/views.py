import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import RegistrationForm
from .models import Guest
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def landing_page(request):
    """
    Renders the beautiful, responsive landing page. This is the new entry point
    for the website.
    """
    return render(request, 'party_register_app/landing_page.html')


def register_guest(request):
    """
    Handles the display and processing of the guest registration form.
    This view is now accessed at the '/register/' URL.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if the guest consented to coming
            if form.cleaned_data['will_attend']:
                guest = form.save()
                # Redirect to the success page, passing the new guest's unique ID
                return redirect('registration_success', guest_uuid=guest.unique_id)
            else:
                # If they select "No", show a "thanks anyway" page
                return render(request, 'party_register_app/no_thanks.html')
    else:
        # If it's a GET request, create a new empty form
        form = RegistrationForm()
    # Render the registration page with the form
    return render(request, 'party_register_app/register.html', {'form': form})


def registration_success(request, guest_uuid):
    """
    Shows the success message and a unique QR code for the registered guest.
    """
    # Find the specific guest using the UUID from the URL, or show a 404 error
    guest = get_object_or_404(Guest, unique_id=guest_uuid)

    # 1. Generate the URL that the QR code will point to.
    #    This URL must be absolute (e.g., https://yourdomain.com/checkin/...)
    check_in_url = request.build_absolute_uri(
        reverse('check_in_detail', args=[str(guest.unique_id)])
    )

    # 2. Generate the QR Code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(check_in_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 3. Save the QR code to an in-memory buffer and encode it as Base64.
    #    This allows us to embed the image directly in the HTML template.
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'guest': guest,
        'qr_code_base64': qr_code_base64,
    }
    return render(request, 'party_register_app/success.html', context)


def check_in(request, guest_uuid=None):
    """
    Handles both the QR code scanner page and the guest detail/check-in page.
    - If guest_uuid is None, it renders the scanner.
    - If guest_uuid is provided, it shows the guest's details or a failure page.
    """
    if guest_uuid is None:
        # Case 1: No UUID provided, show the QR scanner page.
        return render(request, 'party_register_app/check_in_scanner.html')
    else:
        # Case 2: A UUID is in the URL, try to find the guest.
        try:
            guest = Guest.objects.get(unique_id=guest_uuid)
            
            # Handle the check-in form submission
            if request.method == 'POST':
                if guest.status == Guest.Status.VALID:
                    guest.status = Guest.Status.ENTERED
                    guest.save()
                return redirect('party_register_app:check_in_detail', guest_uuid=guest.unique_id)
            
            # For a GET request, show the guest's details
            context = {'guest': guest}
            return render(request, 'party_register_app/check_in_detail.html', context)
            
        except Guest.DoesNotExist:
            # Case 3: The UUID is invalid, show a failure page.
            return render(request, 'party_register_app/check_in_fail.html')

def download_ticket_pdf(request, guest_uuid):
    """
    Generates a beautiful PDF ticket for a given guest and serves it for download.
    """
    guest = get_object_or_404(Guest, unique_id=guest_uuid)

    # --- Re-generate QR Code for the PDF ---
    # We need to do this again here because this is a separate request
    check_in_url = request.build_absolute_uri(reverse('check_in_detail', args=[str(guest.unique_id)]))
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(check_in_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # --- End QR Code Generation ---

    context = {
        'guest': guest,
        'qr_code_base64': qr_code_base64,
    }
    
    # Render the HTML template for the ticket
    html_string = render_to_string('party_register_app/ticket.html', context)
    
    # Use WeasyPrint to create the PDF in memory
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    # Create the HTTP response to trigger a download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket-{guest.name.replace(" ", "-").lower()}.pdf"'
    
    return response
