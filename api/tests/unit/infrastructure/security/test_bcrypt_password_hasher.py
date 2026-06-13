from expects import be_false, be_true, expect, not_

from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

PASSWORD = "secret-password"


class TestBcryptPasswordHasher:
    def test_hash_never_contains_the_plain_text_password(self) -> None:
        hasher = BcryptPasswordHasher()

        password_hash = hasher.hash(PASSWORD)

        expect(PASSWORD in password_hash).to(be_false)
        expect(password_hash == PASSWORD).to(not_(be_true))

    def test_verify_accepts_the_original_password(self) -> None:
        hasher = BcryptPasswordHasher()

        password_hash = hasher.hash(PASSWORD)

        expect(hasher.verify(PASSWORD, password_hash)).to(be_true)

    def test_verify_rejects_a_wrong_password(self) -> None:
        hasher = BcryptPasswordHasher()

        password_hash = hasher.hash(PASSWORD)

        expect(hasher.verify("another-password", password_hash)).to(be_false)

    def test_verify_rejects_a_malformed_hash(self) -> None:
        hasher = BcryptPasswordHasher()

        expect(hasher.verify(PASSWORD, "not-a-bcrypt-hash")).to(be_false)
