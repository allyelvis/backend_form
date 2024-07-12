<!-- invoice_form.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Invoice Form - Aenzbi</title>
</head>
<body>
    <h1>Invoice Form - Aenzbi</h1>
    <form id="invoiceForm">
        <fieldset>
            <legend>A. Identification du vendeur</legend>
            Nom et prénom ou Raison sociale: <input type="text" id="sellerName" required><br>
            NIF: <input type="text" id="sellerNIF" required><br>
            Registre de Commerce N°: <input type="text" id="sellerRegistre" required><br>
            B.P: <input type="text" id="sellerBP"><br>
            Téléphone: <input type="text" id="sellerPhone"><br>
            Commune: <input type="text" id="sellerCommune"><br>
            Quartier: <input type="text" id="sellerQuartier"><br>
            Av.: <input type="text" id="sellerAvenue"><br>
            Rue: <input type="text" id="sellerRue"><br>
            N°: <input type="text" id="sellerNumber"><br>
            Assujetti à la TVA: <input type="checkbox" id="sellerTVA"><br>
        </fieldset>

        <fieldset>
            <legend>B. Le client</legend>
            Nom et prénom ou Raison sociale: <input type="text" id="clientName" required><br>
            NIF: <input type="text" id="clientNIF" required><br>
            Résident à: <input type="text" id="clientResident"><br>
            Assujetti à la TVA: <input type="checkbox" id="clientTVA"><br>
        </fieldset>

        <fieldset>
            <legend>Invoice Details</legend>
            <table id="invoiceTable">
                <tr>
                    <th>Nature de l’article ou service</th>
                    <th>Qté</th>
                    <th>PU</th>
                    <th>PVHTVA</th>
                </tr>
                <tr>
                    <td><input type="text" name="article" required></td>
                    <td><input type="number" name="quantity" required></td>
                    <td><input type="number" name="price" required></td>
                    <td><input type="number" name="total" required></td>
                </tr>
            </table>
        </fieldset>

        <button type="button" onclick="submitForm()">Submit</button>
    </form>

    <script>
        function submitForm() {
            const form = document.getElementById('invoiceForm');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            fetch('https://ebms.obr.gov.bi:9443/ebms_api/addInvoice', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer YOUR_TOKEN_HERE',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    alert('Invoice posted successfully!');
                } else {
                    alert('Failed to post invoice.');
                }
            });
        }
    </script>
    <footer>&copy; Aenzbi</footer>
</body>
</html>
