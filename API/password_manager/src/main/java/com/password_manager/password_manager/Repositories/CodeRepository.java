package com.password_manager.password_manager.Repositories;

import com.password_manager.password_manager.models.CodeModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CodeRepository extends JpaRepository<CodeModel, UUID> {
    @Query("SELECT code from CodeModel code where code.userModel.id = :id")
    List<CodeModel> findByUserModel(UUID id);

    Optional<CodeModel> findById(UUID id);
    Optional<CodeModel> findByCode(String code);
}
