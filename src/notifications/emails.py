import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from database.models import PaymentModel
from exceptions import BaseEmailError
from notifications.interfaces import EmailSenderInterface


class EmailSender(EmailSenderInterface):
    def __init__(
        self,
        hostname: str,
        port: int,
        email: str,
        password: str,
        use_tls: bool,
    ):
        self._hostname = hostname
        self._port = port
        self._email = email
        self._password = password
        self._use_tls = use_tls

    async def _send_email(
        self, recipient: str, subject: str, text_content: str
    ) -> None:
        """
        Asynchronously send an email with the given subject and plain text content.

        Args:
            recipient (str): The recipient's email address.
            subject (str): The subject of the email.
            text_content (str): The plain text content of the email.

        Raises:
            BaseEmailError: If sending the email fails.
        """
        message = MIMEMultipart()
        message["From"] = self._email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(text_content, "plain"))

        try:
            smtp = aiosmtplib.SMTP(
                hostname=self._hostname, port=self._port, start_tls=self._use_tls
            )
            await smtp.connect()
            await smtp.login(self._email, self._password)
            await smtp.sendmail(self._email, [recipient], message.as_string())
            await smtp.quit()
        except aiosmtplib.SMTPException as error:
            logging.error(f"Failed to send email to {recipient}: {error}")
            raise BaseEmailError(f"Failed to send email to {recipient}: {error}")

    async def send_activation_email(self, email: str, activation_token: str) -> None:
        subject = "Activate Your Account"
        activation_link = "http://127.0.0.1/accounts/activate/"
        text_content = (
            f"Hello,\n\n"
            f"Please activate your account using the following link: {activation_link}\n\n"
            f"To activate your account, use this token: {activation_token}\n\n"
            f"Best regards,\nZimBABE Team"
        )
        await self._send_email(email, subject, text_content)

    async def send_password_reset_email(
        self, email: str, reset_token_complete: str
    ) -> None:
        subject = "Password Reset Request"
        reset_link = "http://127.0.0.1/accounts//reset-password/complete/"
        text_content = (
            f"Hello,\n\nYou requested a password reset. Use the following link to reset your password: {reset_link}\n\n "
            f"You can use this token to reset your password: {reset_token_complete}\n\nBest regards,\nZimBABE Team"
        )
        await self._send_email(email, subject, text_content)

    async def send_payment_complete_email(
        self, email: str, payment: PaymentModel
    ) -> None:
        subject = "Payment Complete"
        text_content = (
            f"Hello,\n\n"
            f"Your payment was successful.\n\n"
            f"Payment №{payment.id}\n"
            f"Order №{payment.order_id} - {payment.amount}$\n\n"
            f"Best regards,\nZimBABE Team"
        )

        await self._send_email(email, subject, text_content)
