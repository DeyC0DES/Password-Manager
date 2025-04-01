package com.password_manager.password_manager.Repositories;

import com.password_manager.password_manager.models.AccountModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface AccountRepository extends JpaRepository<AccountModel, UUID> {

    @Query("SELECT account from AccountModel account where account.userModel.id = :id")
    List<AccountModel> findByUserModel(UUID id);

    Optional<AccountModel> findById(UUID id);
    Optional<AccountModel> findByAccountName(String accountName);
}
