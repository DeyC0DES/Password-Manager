package com.password_manager.password_manager.services;

import com.password_manager.password_manager.Repositories.AccountRepository;
import com.password_manager.password_manager.models.AccountModel;
import jakarta.transaction.Transactional;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class AccountService {

    private final AccountRepository accountRepository;

    public AccountService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    // requests
    @Transactional
    public void save(AccountModel accountModel) {
        this.accountRepository.save(accountModel);
    }

    public Optional<AccountModel> findById(UUID id) {
        return this.accountRepository.findById(id);
    }

    public List<AccountModel> findByUserModel(UUID id) {
        return this.accountRepository.findByUserModel(id);
    }

    public Optional<AccountModel> findByAccountName(String accountName) {
        return this.accountRepository.findByAccountName(accountName);
    }

    public ResponseEntity<Object> delete(AccountModel accountModel) {
        this.accountRepository.delete(accountModel);
        return ResponseEntity.ok("Account deleted");
    }
}
